
该工具集提供了以下功能：
1. 将给定的IP地址范围精确转换为CIDR列表。
2. 根据给定的新前缀生成子网。
3. 可将结果输出到TXT格式的文件中。

======================================================================================
      ::::::::::: :::::::::      ::::::::::: ::::::::   ::::::::  :::        :::::::: 
         :+:     :+:    :+:         :+:    :+:    :+: :+:    :+: :+:       :+:    :+: 
        +:+     :+:    :+:         :+:    :+:    +:+ +:+    :+: +:+       +:+         
       +#+     +#++:++#+          +#+    :+:    +:+ +#+    :+: +#+       +#++:++#++   
      +#+     +#+                +#+    :+:    +:+ +#+    :+: +#+              +#+    
     #+#     :+#                #+#    :+:    +:+ #+#    :+: #+#       :+#    :+#     
########### ###                ###     ########   ########  ########## ########         
======================================================================================
                                    作者: MisakiSATA                                    
======================================================================================
usage: ip_tools.py [-h] [--subnet network new_prefix] [--range start_ip end_ip] [--saveas output_path]

IP工具集合，支持子网生成和IP范围转换为CIDR。

options:
  -h, --help            show this help message and exit
  --subnet network new_prefix
                        生成子网：原始网络（例如：192.168.1.0/16）和新的前缀长度（例如：17）。
  --range start_ip end_ip
                        将IP范围转换为CIDR：起始IP地址和结束IP地址。
  --saveas output_path  输出文件路径，如 result.txt