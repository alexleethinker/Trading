from hikyuu.interactive import *
from Strategy.sg.Divergence import *
import matplotlib.pyplot as plt

#创建一个从2022年4月1日开始的账户，初始资金100万元
my_tm = crtTM(date = Datetime(201204010000), init_cash = 1000000, cost_func=TC_FixedA(commission=0.0001, lowest_commission=5.0))
#不做仓位管理，全仓买进卖出
# my_mm = crtMM(MM_Nothing,{'auto-checkin':True})
my_mm = MM_Nothing()
# my_mm = MM_FixedCount()
#回测时间设定
query = Query(Datetime(201204010000), Datetime(202604010000), ktype = 'DAY', recover_type = Query.BACKWARD)

#回测标的限定
s = sm['sz300408']



my_sg = crtSG(SKDJDivergenceSG, 
              {'n': 9, 'm': 3, 'oversold': 55, 'overbought': 50, 'lookback': 20, 'window':4 ,'alternate':False, 'support_borrow_stock': True}, 
              'SKDJ背离策略')


sys = SYS_Simple(tm = my_tm, mm = my_mm, sg = my_sg)
sys.run(s, query)


sys.plot()
MA(CLOSE(sys.to), n = 200).plot(new=False)
MA(CLOSE(sys.to), n = 250).plot(new=False)

plt.show()