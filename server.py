import asyncio

DATABASE = {}


def put(data: str):
    data = data.split()
    if data[0] in DATABASE:
        DATABASE[data[0]].append((data[1], data[2]))
    else:
        DATABASE[data[0]] = [(data[1], data[2])]


def get(command: str) -> str:
    key = command.replace("\r", "")

    if key == "*":
        result = "ok\n"
        for key, data in DATABASE.items():

            for value in data:
                result += "{} {} {}\n".format(key, value[0], value[1])

        return result + "\n"

    if key in DATABASE:
        data = DATABASE[key]
        result = "ok\n"
        for value in data:
            result += "{} {} {}\n".format(key, value[0], value[1])
        return result + "\n"
    else:
        return "ok\n\n"


def process_data(data: str) -> str:
    rep_data = data.replace("\n", "")[4:]
    command = data[:3]

    if command == "get":
        return get(rep_data)
    elif command == "put":
        put(rep_data)
        return "ok\n\n"
    else:
        return "error\nwrong command\n\n"


class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data: bytes):
        resp = process_data(data.decode())
        self.transport.write(resp.encode())


def run_server(host: str, port: int):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
