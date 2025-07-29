from typing import Iterable, Literal

import grpc
from google.protobuf.duration_pb2 import Duration
from google.protobuf.struct_pb2 import Struct
from google.protobuf.timestamp_pb2 import Timestamp

from . import beaker_pb2 as pb2
from ._service_client import RpcMethod, RpcStreamingMethod, ServiceClient
from .exceptions import BeakerQueueNotFound
from .types import *


class QueueClient(ServiceClient):
    def get(self, queue_id: str) -> pb2.Queue:
        return self.rpc_request(
            RpcMethod[pb2.GetQueueResponse](self.service.GetQueue),
            pb2.GetQueueRequest(queue_id=self.resolve_queue_id(queue_id)),
            exceptions_for_status={grpc.StatusCode.NOT_FOUND: BeakerQueueNotFound(queue_id)},
        ).queue

    def create(
        self,
        name: str | None = None,
        workspace: pb2.Workspace | None = None,
        input_schema: dict | None = {},
        output_schema: dict | None = {},
        batch_size: int | None = 1,
        max_claimed_entries: int | None = 1,
        wait_timeout_ms: int | None = 0,
    ) -> pb2.Queue:
        wait_timeout = None
        if wait_timeout_ms is not None:
            wait_timeout = Duration()
            wait_timeout.FromMilliseconds(wait_timeout_ms)
        input_schema_struct = Struct()
        if input_schema is not None:
            input_schema_struct.update(input_schema)
        output_schema_struct = Struct()
        if output_schema is not None:
            output_schema_struct.update(output_schema)
        return self.rpc_request(
            RpcMethod[pb2.CreateQueueResponse](self.service.CreateQueue),
            pb2.CreateQueueRequest(
                workspace_id=self.resolve_workspace_id(workspace),
                name=name,
                input_schema=input_schema_struct,
                output_schema=output_schema_struct,
                batch_size=batch_size,
                max_claimed_entries=max_claimed_entries,
                wait_timeout=wait_timeout,
            ),
        ).queue

    def delete(
        self,
        *queues: pb2.Queue,
    ):
        self.rpc_request(
            RpcMethod[pb2.DeleteQueuesResponse](self.service.DeleteQueues),
            pb2.DeleteQueuesRequest(queue_ids=[self.resolve_queue_id(q) for q in queues]),
        )

    def list(
        self,
        *,
        org: pb2.Organization | None = None,
        workspace: pb2.Workspace | None = None,
        sort_order: BeakerSortOrder | None = BeakerSortOrder.descending,
        sort_field: Literal["created"] = "created",
        limit: int | None = None,
    ) -> Iterable[pb2.Queue]:
        if limit is not None and limit <= 0:
            raise ValueError("'limit' must be a positive integer")

        count = 0
        for response in self.rpc_paged_request(
            RpcMethod[pb2.ListQueuesResponse](self.service.ListQueues),
            pb2.ListQueuesRequest(
                options=pb2.ListQueuesRequest.Opts(
                    sort_clause=pb2.ListQueuesRequest.Opts.SortClause(
                        sort_order=None if sort_order is None else sort_order.as_pb2(),
                        created={} if sort_field == "created" else None,
                    ),
                    organization_id=self.resolve_org_id(org),
                    workspace_id=None
                    if workspace is None
                    else self.resolve_workspace_id(workspace),
                    page_size=self.MAX_PAGE_SIZE
                    if limit is None
                    else min(self.MAX_PAGE_SIZE, limit),
                ),
            ),
        ):
            for queue in response.queues:
                count += 1
                yield queue
                if limit is not None and count >= limit:
                    return

    def create_entry(
        self,
        queue: pb2.Queue,
        *,
        input: dict | None = {},
        expires_in_sec: int | None = None,
    ) -> Iterable[pb2.CreateQueueEntryResponse]:
        expiry = None
        if expires_in_sec is not None:
            expiry = Timestamp()
            expiry.GetCurrentTime()
            expiry.FromSeconds(expiry.seconds + expires_in_sec)
        input_struct = Struct()
        if input is not None:
            input_struct.update(input)
        request = pb2.CreateQueueEntryRequest(
            queue_id=self.resolve_queue_id(queue),
            input=input_struct,
            expiry=expiry,
        )
        yield from self.rpc_streaming_request(
            RpcStreamingMethod[pb2.CreateQueueEntryResponse](self.service.CreateQueueEntry),
            request,
            exceptions_for_status={grpc.StatusCode.NOT_FOUND: BeakerQueueNotFound(queue.id)},
        )
