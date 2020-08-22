import asyncio

async def find_divisibles(inrange, div_by):
    print("finding nums in range {} divisible by {}".format(inrange, div_by))
    located = []
    for i in range(inrange):
        if i % div_by == 0:
            located.append(i)
        if i % 50000 == 0:
            await asyncio.sleep(0.03)

    print("Done w/ nums in range {} divisible by {}".format(inrange, div_by))
    return located


async def main():
    temp = {5080000: 34113 , 100052: 3210, 50000: 3}
    listy = []
    for k, v in temp.items():
        i = loop.create_task(find_divisibles(k, v))
        listy.append(i)
    await asyncio.wait(listy)
    # return listy[0], listy[1], listy[2]


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.set_debug(1)
        # d1, d2, d3 = loop.run_until_complete(main())
        # print(d1.result())
        loop.run_until_complete(main())
    except Exception as e:
        # logging...etc
        pass
    finally:
        loop.close()

# temp = {508000: 34113 , 100052: 3210, 500: 3}
# for k, v in temp.items():
#     print(k,v)
