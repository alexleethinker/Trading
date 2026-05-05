from hikyuu.interactive import *
from Uitls.peaks import *

def SKDJDivergenceSG(self, k):
    """
    SKDJ背离策略
    参数说明:
    n: SKDJ周期参数，默认9
    m: K值平滑参数，默认3
    oversold: 超卖阈值，默认20
    overbought: 超买阈值，默认80
    lookback: 背离检测回溯周期，默认20
    """
    # 获取参数
    n = self.get_param("n")
    m = self.get_param("m")
    oversold = self.get_param("oversold")
    overbought = self.get_param("overbought")
    lookback = self.get_param("lookback")
    window = self.get_param("window")
    
    
    # 获取价格数据
    c = CLOSE(k)
    l = LOW(k)
    h = HIGH(k)

    lowv = LLV(l, n)
    highv = HHV(h, n)
    rsv = (c - lowv) / (highv - lowv) * 100
    rsv_slow = EMA(rsv, m)
    skdj_k = EMA(rsv_slow, m)

    # 使用find_phase_extreme_points函数获取阶段低点和高点
    # 这里使用lookback作为窗口参数
    phase_lows, phase_highs = find_phase_peaks(k, window=window, min_depth=0.01)
    
 # 确保有足够数据
    if len(c) < 30 or len(skdj_k) < 30:
        return
    
    # 存储最近的阶段低点和高点
    last_low_point = None
    last_high_point = None
    
    # 遍历K线
    for i in range(window*2, len(k)):
        # 获取当前值
        current_low = l[i]
        current_high = h[i]
        current_skdj_k = skdj_k[i] if i < len(skdj_k) else None
        
        if current_skdj_k is None:
            continue
        
        # 1. 更新最近的阶段低点
        for low_point in phase_lows:
            if low_point['index'] < i-4:
                if last_low_point is None or low_point['index'] > last_low_point['index']:
                    last_low_point = low_point.copy()
                    if low_point['index'] < len(skdj_k):
                        last_low_point['skdj_k'] = skdj_k[low_point['index']]
        
        # 2. 更新最近的阶段高点
        for high_point in phase_highs:
            if high_point['index'] < i:
                if last_high_point is None or high_point['index'] > last_high_point['index']:
                    last_high_point = high_point.copy()
                    if high_point['index'] < len(skdj_k):
                        last_high_point['skdj_k'] = skdj_k[high_point['index']]
        
        # 3. 底背离买入信号
        if (last_low_point is not None and 
            'skdj_k' in last_low_point and
            current_skdj_k < oversold):
            
            # 价格创新低
            price_new_low = current_low < last_low_point['price']
            
            # SKDJ没有创新低
            skdj_not_new_low = current_skdj_k > last_low_point['skdj_k']
            
            # SKDJ开始反转
            skdj_reverse = False
            if i >= 2 and i < len(skdj_k):
                skdj_reverse = skdj_k[i] > skdj_k[i-1]
            
            if price_new_low and skdj_not_new_low and skdj_reverse:
                self._add_buy_signal(k[i].datetime)
        
        # 4. 顶背离卖出信号
        if (last_high_point is not None and 
            'skdj_k' in last_high_point and
            current_skdj_k > overbought):
            
            # 价格创新高
            price_new_high = current_high > last_high_point['price']
            
            # SKDJ没有创新高
            skdj_not_new_high = current_skdj_k < last_high_point['skdj_k']
            
            # SKDJ开始反转
            skdj_reverse = False
            if i >= 2 and i < len(skdj_k):
                skdj_reverse = skdj_k[i] < skdj_k[i-1]
            
            if price_new_high and skdj_not_new_high and skdj_reverse:
                self._add_sell_signal(k[i].datetime)


if __name__ == 'main':

    # 创建策略实例
    my_sg = crtSG(SKDJDivergenceSG, 
                  {'n': 9, 'm': 3, 'oversold': 55, 'overbought': 50, 'lookback': 20, 'window':4 ,'alternate':False, 'support_borrow_stock': True}, 
                  'SKDJ背离策略')