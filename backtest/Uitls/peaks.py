from hikyuu.interactive import *


def find_phase_peaks(k, window=5, min_depth=0.00):
    """
    增强版本：带确认条件的阶段低点和阶段高点寻找
    
    参数：
    k: K线数据
    window: 时间窗口大小
    min_depth: 最小深度（相对周围价格的百分比）
    
    返回：
    (phase_lows, phase_highs) 元组，包含阶段低点和阶段高点信息的列表
    """
    # 获取价格序列
    low_prices = LOW(k)
    high_prices = HIGH(k)
    close_prices = CLOSE(k)
    
    n = len(k)
    phase_lows = []
    phase_highs = []
    
    for i in range(window, n - window):
        # 获取窗口
        start_idx = i - window
        end_idx = i + window + 1
        
        # 1. 阶段低点检测
        # 当前最低价
        current_low = low_prices[i]
        
        # 条件1：是窗口内的最低点
        window_lows = low_prices[start_idx:end_idx]
        if current_low > min(window_lows):
            low_is_extreme = False
        else:
            # 条件2：检查唯一性（严格小于窗口内其他所有最低价）
            is_unique_min = True
            for j in range(start_idx, end_idx):
                if j != i and low_prices[j] <= current_low:
                    is_unique_min = False
                    break
            
            if not is_unique_min:
                low_is_extreme = False
            else:
                # 条件3：最小深度要求
                # 计算窗口内除当前点外的平均最低价
                other_lows = [low_prices[j] for j in range(start_idx, end_idx) if j != i]
                avg_other_lows = sum(other_lows) / len(other_lows) if other_lows else current_low
                
                # 计算深度
                depth = (avg_other_lows - current_low) / avg_other_lows
                if depth < min_depth:
                    low_is_extreme = False
                else:
                    # 条件4：价格形态确认（可选）
                    # 检查是否形成V形底：前几日下跌，后几日上涨
                    is_v_shape = True
                    for offset in range(1, 4):  # 检查前后3日
                        if i - offset >= 0 and i + offset < n:
                            # 前几日应该下跌或持平
                            if close_prices[i-offset] < current_low:
                                is_v_shape = False
                                break
                            # 后几日应该上涨
                            if close_prices[i+offset] < current_low:
                                is_v_shape = False
                                break
                    
                    low_is_extreme = True
        
        # 2. 阶段高点检测
        # 当前最高价
        current_high = high_prices[i]
        
        # 条件1：是窗口内的最高点
        window_highs = high_prices[start_idx:end_idx]
        if current_high < max(window_highs):
            high_is_extreme = False
        else:
            # 条件2：检查唯一性（严格大于窗口内其他所有最高价）
            is_unique_max = True
            for j in range(start_idx, end_idx):
                if j != i and high_prices[j] >= current_high:
                    is_unique_max = False
                    break
            
            if not is_unique_max:
                high_is_extreme = False
            else:
                # 条件3：最小深度要求
                # 计算窗口内除当前点外的平均最高价
                other_highs = [high_prices[j] for j in range(start_idx, end_idx) if j != i]
                avg_other_highs = sum(other_highs) / len(other_highs) if other_highs else current_high
                
                # 计算深度
                depth = (current_high - avg_other_highs) / avg_other_highs
                if depth < min_depth:
                    high_is_extreme = False
                else:
                    # 条件4：价格形态确认（可选）
                    # 检查是否形成倒V形顶：前几日上涨，后几日下跌
                    is_inverse_v_shape = True
                    for offset in range(1, 4):  # 检查前后3日
                        if i - offset >= 0 and i + offset < n:
                            # 前几日应该上涨
                            if close_prices[i-offset] > current_high:
                                is_inverse_v_shape = False
                                break
                            # 后几日应该下跌
                            if close_prices[i+offset] > current_high:
                                is_inverse_v_shape = False
                                break
                    
                    high_is_extreme = True
        
        # 记录符合条件的阶段低点
        if low_is_extreme:
            # 计算周围平均价格（用于深度计算）
            other_lows = [low_prices[j] for j in range(start_idx, end_idx) if j != i]
            avg_other_lows = sum(other_lows) / len(other_lows) if other_lows else current_low
            
            phase_lows.append({
                'index': i,
                'date': k[i].datetime,
                'price': float(current_low),  # 低点价格
                'avg_surrounding': float(avg_other_lows),
                'depth_percent': float(((avg_other_lows - current_low) / avg_other_lows) * 100),
                'is_v_shape': is_v_shape,
                'window_size': 2 * window + 1,
                'type': 'low'  # 标记为低点
            })
        
        # 记录符合条件的阶段高点
        if high_is_extreme:
            # 计算周围平均价格（用于深度计算）
            other_highs = [high_prices[j] for j in range(start_idx, end_idx) if j != i]
            avg_other_highs = sum(other_highs) / len(other_highs) if other_highs else current_high
            
            phase_highs.append({
                'index': i,
                'date': k[i].datetime,
                'price': float(current_high),  # 高点价格
                'avg_surrounding': float(avg_other_highs),
                'depth_percent': float(((current_high - avg_other_highs) / avg_other_highs) * 100),
                'is_inverse_v_shape': is_inverse_v_shape,
                'window_size': 2 * window + 1,
                'type': 'high'  # 标记为高点
            })
    
    return phase_lows, phase_highs

