from mcp.server.fastmcp import FastMCP

mcp = FastMCP("fenda-weather")


@mcp.tool()
def query_weather(city_name: str) -> str:
    """ 根据城市名称获取天气信息

    :param city_name: 城市名称
    :return: 天气信息
    """
    return "你好，%s的天气很好~ 27度不冷不热" % city_name


if __name__ == "__main__":
    mcp.run(transport='stdio')
