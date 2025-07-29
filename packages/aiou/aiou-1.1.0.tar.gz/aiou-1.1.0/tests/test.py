#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from aiou import RedisConnector


async def async_main():
    connector = RedisConnector()
    print('redis connector: %s' % connector)


def main():
    asyncio.run(async_main())


if __name__ == '__main__':
    main()
