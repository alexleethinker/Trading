from mootdx.affair import Affair

# 远程文件列表
files = Affair.files()

# 下载单个
Affair.fetch(downdir='tmp', filename='gpcw20240331.zip')
result = Affair.parse(downdir='tmp', filename='gpcw20240331.zip')

# # 下载全部
# Affair.parse(downdir='tmp')


mootdx affair -f gpcw20240331.zip -o gpcw20240331.csv
