#!/usr/bin/python3
"""
IP工具集合
作者: MisakiSATA

该工具集提供了以下功能：
1. 将给定的IP地址范围精确转换为CIDR列表。
2. 根据给定的新前缀生成子网。
3. 可将结果输出到TXT格式的文件中。
"""

import ipaddress
import argparse


def range_to_cidr(start_ip, end_ip):
    """
    将给定的IP地址范围转换为精确匹配的CIDR列表。
    """
    try:
        start = ipaddress.IPv4Address(start_ip)
        end = ipaddress.IPv4Address(end_ip)
    except ipaddress.AddressValueError:
        raise ValueError("无效的IP地址格式，请检查输入的起始IP和结束IP地址是否正确。")

    if start > end:
        raise ValueError("起始IP地址必须小于或等于结束IP地址。")

    cidrs = []
    current_ip = start

    while current_ip <= end:
        max_prefix_length = 32  # 初始值
        for prefix_length in range(1, 33):  # 从小到大尝试前缀
            network = ipaddress.IPv4Network(f"{current_ip}/{prefix_length}", strict=False)
            # 检查网络块是否满足条件：覆盖当前 IP 且不超出范围
            if network.network_address == current_ip and network.broadcast_address <= end:
                max_prefix_length = prefix_length
                break
        # 添加当前找到的最大网络块
        cidrs.append(f"{network.network_address}/{max_prefix_length}")
        # 更新 current_ip 为下一个网络块的起始地址
        current_ip = network.broadcast_address + 1

    return cidrs


def generate_subnets(target, prefix):
    """
    根据给定的新前缀生成子网。

    :param target: 原始网络地址，字符串格式，如 "192.168.1.0/16"
    :param prefix: 新的前缀长度，字符串格式，需可转换为整数
    :return: 生成的子网列表，每个元素为IPv4Network对象
    """
    try:
        original_network = ipaddress.ip_network(target, strict=False)
        prefix = int(prefix)
    except ValueError:
        raise ValueError("请提供有效的网络地址或前缀长度。")

    if prefix <= original_network.prefixlen:
        raise ValueError("新前缀必须比原始前缀长。")

    return list(original_network.subnets(new_prefix=prefix))


def print_icon():
    """
    输出图标和作者信息。
    """
    icon = [
        "      ::::::::::: :::::::::      ::::::::::: ::::::::   ::::::::  :::        :::::::: ",
        "         :+:     :+:    :+:         :+:    :+:    :+: :+:    :+: :+:       :+:    :+: ",
        "        +:+     :+:    :+:         :+:    :+:    +:+ +:+    :+: +:+       +:+         ",
        "       +#+     +#++:++#+          +#+    :+:    +:+ +#+    :+: +#+       +#++:++#++   ",
        "      +#+     +#+                +#+    :+:    +:+ +#+    :+: +#+              +#+    ",
        "     #+#     :+#                #+#    :+:    +:+ #+#    :+: #+#       :+#    :+#     ",
        "########### ###                ###     ########   ########  ########## ########         "
    ]

    border_length = len(icon[0])
    border = "=" * border_length
    print(border)
    for line in icon:
        print(line)
    print(border)

    # 输出居中的作者信息
    author = "作者: MisakiSATA"
    print(author.center(border_length))
    print(border)


def output_to_file(data, output_file_path):
    """
    将数据输出到TXT格式的文件。

    :param data: 要输出的数据，可以是CIDR列表或子网列表等
    :param output_file_path: 输出文件路径
    """
    with open(output_file_path, 'w') as f:
        for item in data:
            f.write(f"{item}\n")


def main():
    """
    主函数，程序的入口点。
    """
    # 在程序启动时输出图标和作者信息
    print_icon()

    parser = argparse.ArgumentParser(description="IP工具集合，支持子网生成和IP范围转换为CIDR。")
    parser.add_argument('--subnet', nargs=2, metavar=('network', 'new_prefix'),
                        help="生成子网：原始网络（例如：192.168.1.0/16）和新的前缀长度（例如：17）。")
    parser.add_argument('--range', nargs=2, metavar=('start_ip', 'end_ip'),
                        help="将IP范围转换为CIDR：起始IP地址和结束IP地址。")
    parser.add_argument('--saveas', metavar='output_path',
                        help="输出文件路径，如 result.txt")

    args = parser.parse_args()

    # 如果未提供任何参数，打印帮助信息并退出
    if not args.subnet and not args.range:
        parser.print_help()
        exit(1)

    output_path = args.saveas if args.saveas else None

    # 处理生成子网的逻辑
    if args.subnet:
        try:
            subnets = generate_subnets(args.subnet[0], args.subnet[1])
            print("\n生成的子网：")
            for subnet in subnets:
                print(f"{subnet}")
            if output_path:
                output_to_file(subnets, output_path)
        except ValueError as e:
            print(f"发生错误：{e}")

    # 处理 IP 范围转换为CIDR的逻辑
    if args.range:
        try:
            cidrs = range_to_cidr(args.range[0], args.range[1])
            print("\n转换结果的CIDR列表：")
            for cidr in cidrs:
                print(f"{cidr}")
            if output_path:
                output_to_file(cidrs, output_path)
        except ValueError as e:
            print(f"发生错误：{e}")


if __name__ == "__main__":
    main()