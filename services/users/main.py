from common.lib.rpc import ServiceResolver


class UserService(ServiceResolver):
    async def start(self):
        print("run user service")

    async def show_users(self): ...
