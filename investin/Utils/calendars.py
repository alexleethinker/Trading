import cloudscraper
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')
try:
    from investin.Utils.config import data_dir
except:
    data_dir = 'investin/data'
 
save_path = data_dir + '/spot/dividends_splits.csv'
tqdm.pandas()

today = datetime.today().strftime("%Y-%m-%d")
scraper = cloudscraper.create_scraper(browser={'browser':'firefox','platform':'windows','mobile':'false'})

  
def country_dic():
    country_list = [4,5,6,7,9,10,11,12,14,15,17,20,21,22,23,24,25,26,\
                    27,29,32,33,34,35,36,37,38,39,41,42,43,44,45,46,47,\
                    48,51,52,53,54,55,56,57,59,60,61,63,66,68,70,71,72,75,\
                    78,80,84,85,87,89,90,92,93,94,96,97,100,102,103,105,106,\
                    107,109,110,111,112,113,119,122,123,125,138,139,143,145,\
                    162,163,170,172,174,178,188,193,202,238,247]
    dic = ''
    for i in country_list:
        dic += f'country%5B%5D={i}&'
    return dic
    
    
def get_today_calendar(event):
    headers = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,ja;q=0.6,zh-TW;q=0.5,nl;q=0.4',
        'Content-Length':'100',
        'Content-Type':'application/x-www-form-urlencoded',
        'Cookie':'PHPSESSID=ppbe37qspnmfbfq5saq8je134q; geoC=NL; page_equity_viewed=0; browser-session-counted=true; user-browser-sessions=1; adBlockerNewUserDomains=1695904424; udid=3e9c3a53fb8e26dc5b74c8f318f24294; smd=3e9c3a53fb8e26dc5b74c8f318f24294-1695904424; __cflb=02DiuGRugds2TUWHMkkPGro65dgYiP187jUhdXQKxEPBr; _gid=GA1.2.1815319210.1695904425; OptanonAlertBoxClosed=2023-09-28T12:33:46.582Z; eupubconsent-v2=CPyznrAPyznrAAcABBENDYCsAP_AAH_AAChQJrNf_X__b2_r-_7_f_t0eY1P9_7__-0zjhfdF-8N3f_X_L8X52M5vF36tqoKuR4ku3bBIUdlHPHcTVmw6okVryPsbk2cr7NKJ7PkmlMbM2dYGH9_n9_z-ZKY7___f__z_v-v___9____7-3f3__5__--__e_V_-9zfn9_____9vP___9v-_9_3________3_r9_7_D_-f_87_XW-8QUACTDQuIAuyJGQm2jCKBACMKwkKoFABRAJC0QGELq4KdlcBPrARACBFAA8EAIYAUZAAgAAEgCQiACQI4EAgEAgEAAIAFQgEADGwADwAtBAIABQHQsU4oAlAsIMiMiIUwIQpEgoJ7KhBKD9QVwhDLLAig0f8VCAhWQMVgRCQsXocASAl4kkD3VG-AAhACgFFKFYik_MAQ4Jmy1V4oAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAA.f_gAD_gAAAAA; OTAdditionalConsentString=1~43.46.55.61.70.83.89.93.108.117.122.124.135.136.143.144.147.149.159.192.196.202.211.228.230.239.259.266.286.291.311.317.322.323.327.338.367.371.385.394.397.407.413.415.424.430.436.445.453.482.486.491.494.495.522.523.540.550.559.560.568.574.576.584.587.591.737.802.803.820.821.839.864.899.904.922.931.938.979.981.985.1003.1027.1031.1040.1046.1051.1053.1067.1085.1092.1095.1097.1099.1107.1135.1143.1149.1152.1162.1166.1186.1188.1201.1205.1215.1226.1227.1230.1252.1268.1270.1276.1284.1290.1301.1307.1312.1345.1356.1364.1365.1375.1403.1415.1416.1421.1440.1449.1455.1495.1512.1516.1525.1540.1548.1555.1558.1570.1577.1579.1583.1584.1591.1603.1616.1638.1651.1653.1667.1677.1678.1682.1697.1699.1703.1712.1716.1721.1725.1732.1745.1750.1765.1769.1782.1786.1800.1810.1825.1827.1832.1838.1840.1842.1843.1845.1859.1866.1870.1878.1880.1889.1899.1917.1929.1942.1944.1962.1963.1964.1967.1968.1969.1978.2003.2007.2008.2027.2035.2039.2047.2052.2056.2064.2068.2072.2074.2088.2090.2103.2107.2109.2115.2124.2130.2133.2135.2137.2140.2145.2147.2150.2156.2166.2177.2183.2186.2205.2216.2219.2220.2222.2225.2234.2253.2279.2282.2292.2299.2305.2309.2312.2316.2322.2325.2328.2331.2334.2335.2336.2337.2343.2354.2357.2358.2359.2370.2376.2377.2387.2392.2400.2403.2405.2407.2411.2414.2416.2418.2425.2440.2447.2461.2462.2465.2468.2472.2477.2481.2484.2486.2488.2493.2498.2499.2501.2510.2517.2526.2527.2532.2535.2542.2552.2563.2564.2567.2568.2569.2571.2572.2575.2577.2583.2584.2596.2604.2605.2608.2609.2610.2612.2614.2621.2628.2629.2633.2636.2642.2643.2645.2646.2650.2651.2652.2656.2657.2658.2660.2661.2669.2670.2677.2681.2684.2687.2690.2695.2698.2713.2714.2729.2739.2767.2768.2770.2772.2784.2787.2791.2792.2798.2801.2805.2812.2813.2816.2817.2821.2822.2827.2830.2831.2834.2838.2839.2844.2846.2849.2850.2852.2854.2860.2862.2863.2865.2867.2869.2873.2874.2875.2876.2878.2880.2881.2882.2883.2884.2886.2887.2888.2889.2891.2893.2894.2895.2897.2898.2900.2901.2908.2909.2913.2914.2916.2917.2918.2919.2920.2922.2923.2927.2929.2930.2931.2940.2941.2947.2949.2950.2956.2958.2961.2963.2964.2965.2966.2968.2973.2975.2979.2980.2981.2983.2985.2986.2987.2994.2995.2997.2999.3000.3002.3003.3005.3008.3009.3010.3012.3016.3017.3018.3019.3024.3025.3028.3034.3037.3038.3043.3048.3052.3053.3055.3058.3059.3063.3066.3068.3070.3073.3074.3075.3076.3077.3078.3089.3090.3093.3094.3095.3097.3099.3104.3106.3109.3112.3117.3119.3126.3127.3128.3130.3135.3136.3145.3150.3151.3154.3155.3163.3167.3172.3173.3182.3183.3184.3185.3187.3188.3189.3190.3194.3196.3209.3210.3211.3214.3215.3217.3219.3222.3223.3225.3226.3227.3228.3230.3231.3234.3235.3236.3237.3238.3240.3244.3245.3250.3251.3253.3257.3260.3268.3270.3272.3281.3288.3290.3292.3293.3295.3296.3299.3300.3306.3307.3314.3315.3316.3318.3324.3327.3328.3330.3331.3531.3731.3831.3931.4131.4531.4631.4731.4831.5031.5231.6931.7031.7235.7831.7931.8931.9731.10231.10631.11031.11531.12831.13632; usprivacy=1YNN; _imntz_error=0; editionPostpone=1695904428925; gtmFired=OK; g_state={"i_p":1695911666208,"i_l":1}; r_p_s_n=1; adsFreeSalePopUp=3; connectId={"lastUsed":1695904544235,"lastSynced":1695904544235}; _cc_id=a8848c7c36356486a869d187657dcb80; panoramaId_expiry=1695990944268; panoramaId=7276961a789524cd91d5264f8549a9fb927a5c09636c5c3a44d6d6de0d6c8174; panoramaIdType=panoDevice; cto_bundle=gE_40l9KcmJNZ1ltSlhIRGxrZmRBMUkxaVllQ1hETHNwQnNJVVBlQzFpMEJHU1lIbVFFenVYbUwwRjlSN0xGVTVmNWRQVmZTa2RJbHY4OFQxNjk3VFNTNEZLY0J0aVBiamRRb1VqaWZobmZoTDE3U045Y1FtVk1XRkhvNTdZRjh4UkJxQWNBOUdYS3BNZ21HbXA0Q2JtNG8yYmExeW04SXI1S3N5ZTloenlSa2NZbHJQVSUyQnliS2VVZWxCdkdCcjV4SmU4bTRXMXNUWXFrMUJBMFZxQTYlMkZHRDJIUSUzRCUzRA; nyxDorf=YmZjNDJnNXdjNGFqNWFjf2IyN21iZzomMDBhYzYx; page_view_count=5; invpc=5; _ga=GA1.1.1499573541.1695904425; _ga_C4NDLGKVMK=GS1.1.1695904424.1.1.1695905631.44.0.0; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Sep+28+2023+14%3A53%3A51+GMT%2B0200+(Central+European+Summer+Time)&version=202303.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=844e0ccc-65b9-4e27-b898-b92b1fe5aa82&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CSTACK42%3A1&geolocation=NL%3BZH&AwaitingReconsent=false; _gat_allSitesTracker=1',
        'Origin':'https://www.investing.com',
        'Pragma':'no-cache',
        'Referer':'https://www.investing.com/stock-split-calendar/',
        'Sec-Ch-Ua':'"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'Sec-Ch-Ua-Mobile':'?0',
        'Sec-Ch-Ua-Platform':"macOS",
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'X-Requested-With':'XMLHttpRequest',
    }  
    url = f'https://www.investing.com/{event}-calendar/Service/getCalendarFilteredData'
    dic=country_dic()
    params = f'{dic}dateFrom={today}&dateTo={today}&currentTab=custom&submitFilters=1&limit_from=0'
    r = scraper.post(url, data=params, headers=headers,timeout=30)
    html = r.json()['data'].replace('\t','').replace('\n','')
    soup = BeautifulSoup(html, "html.parser")
    
    symbol_list  = [i.text for i in soup.select(".left a.bold")]
    
    if event == 'stock-split':
        country_list = [i.get('class')[1] for i in soup.select(".left span.ceFlags")]
        split_list = [i.text for i in soup.select("td:nth-of-type(3)")]
        href = [i.get('href').replace('/equities/','').replace('-dividends','')  for i in soup.select(".left a.bold")]
        df = pd.DataFrame({'country':country_list,'symbol':symbol_list, 'split_ratio':split_list, 'href':href})
    elif event == 'dividends':
        country_list = [i.get('class')[1] for i in soup.select(".flag span")]
        ex_date  = [i.text for i in soup.select("td:nth-of-type(3)")]
        dividend = [i.text for i in soup.select("td:nth-of-type(4)")]
        payment_date = [i.text for i in soup.select("td:nth-of-type(6)")]
        yeild = [i.text for i in soup.select("td:nth-of-type(7)")]
        type = [i.get('title') for i in soup.select("td.textNum span")]
        href = [i.get('href').replace('/equities/','').replace('-dividends','')  for i in soup.select(".left a.bold")]
        df = pd.DataFrame({'country':country_list, 'symbol':symbol_list, 
                   'ex_date':ex_date, 'dividend':dividend, 'type':type,
                   'payment_date':payment_date, 'yeild':yeild, 'href':href
                  })
    return df


def get_stock_details(code):
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,ja;q=0.6,zh-TW;q=0.5,nl;q=0.4',
        'Cache-Control':'max-age=0',
        'Cookie':'PHPSESSID=ppbe37qspnmfbfq5saq8je134q; geoC=NL; page_equity_viewed=0; browser-session-counted=true; user-browser-sessions=1; adBlockerNewUserDomains=1695904424; udid=3e9c3a53fb8e26dc5b74c8f318f24294; smd=3e9c3a53fb8e26dc5b74c8f318f24294-1695904424; __cflb=02DiuGRugds2TUWHMkkPGro65dgYiP187jUhdXQKxEPBr; _gid=GA1.2.1815319210.1695904425; OptanonAlertBoxClosed=2023-09-28T12:33:46.582Z; eupubconsent-v2=CPyznrAPyznrAAcABBENDYCsAP_AAH_AAChQJrNf_X__b2_r-_7_f_t0eY1P9_7__-0zjhfdF-8N3f_X_L8X52M5vF36tqoKuR4ku3bBIUdlHPHcTVmw6okVryPsbk2cr7NKJ7PkmlMbM2dYGH9_n9_z-ZKY7___f__z_v-v___9____7-3f3__5__--__e_V_-9zfn9_____9vP___9v-_9_3________3_r9_7_D_-f_87_XW-8QUACTDQuIAuyJGQm2jCKBACMKwkKoFABRAJC0QGELq4KdlcBPrARACBFAA8EAIYAUZAAgAAEgCQiACQI4EAgEAgEAAIAFQgEADGwADwAtBAIABQHQsU4oAlAsIMiMiIUwIQpEgoJ7KhBKD9QVwhDLLAig0f8VCAhWQMVgRCQsXocASAl4kkD3VG-AAhACgFFKFYik_MAQ4Jmy1V4oAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAA.f_gAD_gAAAAA; OTAdditionalConsentString=1~43.46.55.61.70.83.89.93.108.117.122.124.135.136.143.144.147.149.159.192.196.202.211.228.230.239.259.266.286.291.311.317.322.323.327.338.367.371.385.394.397.407.413.415.424.430.436.445.453.482.486.491.494.495.522.523.540.550.559.560.568.574.576.584.587.591.737.802.803.820.821.839.864.899.904.922.931.938.979.981.985.1003.1027.1031.1040.1046.1051.1053.1067.1085.1092.1095.1097.1099.1107.1135.1143.1149.1152.1162.1166.1186.1188.1201.1205.1215.1226.1227.1230.1252.1268.1270.1276.1284.1290.1301.1307.1312.1345.1356.1364.1365.1375.1403.1415.1416.1421.1440.1449.1455.1495.1512.1516.1525.1540.1548.1555.1558.1570.1577.1579.1583.1584.1591.1603.1616.1638.1651.1653.1667.1677.1678.1682.1697.1699.1703.1712.1716.1721.1725.1732.1745.1750.1765.1769.1782.1786.1800.1810.1825.1827.1832.1838.1840.1842.1843.1845.1859.1866.1870.1878.1880.1889.1899.1917.1929.1942.1944.1962.1963.1964.1967.1968.1969.1978.2003.2007.2008.2027.2035.2039.2047.2052.2056.2064.2068.2072.2074.2088.2090.2103.2107.2109.2115.2124.2130.2133.2135.2137.2140.2145.2147.2150.2156.2166.2177.2183.2186.2205.2216.2219.2220.2222.2225.2234.2253.2279.2282.2292.2299.2305.2309.2312.2316.2322.2325.2328.2331.2334.2335.2336.2337.2343.2354.2357.2358.2359.2370.2376.2377.2387.2392.2400.2403.2405.2407.2411.2414.2416.2418.2425.2440.2447.2461.2462.2465.2468.2472.2477.2481.2484.2486.2488.2493.2498.2499.2501.2510.2517.2526.2527.2532.2535.2542.2552.2563.2564.2567.2568.2569.2571.2572.2575.2577.2583.2584.2596.2604.2605.2608.2609.2610.2612.2614.2621.2628.2629.2633.2636.2642.2643.2645.2646.2650.2651.2652.2656.2657.2658.2660.2661.2669.2670.2677.2681.2684.2687.2690.2695.2698.2713.2714.2729.2739.2767.2768.2770.2772.2784.2787.2791.2792.2798.2801.2805.2812.2813.2816.2817.2821.2822.2827.2830.2831.2834.2838.2839.2844.2846.2849.2850.2852.2854.2860.2862.2863.2865.2867.2869.2873.2874.2875.2876.2878.2880.2881.2882.2883.2884.2886.2887.2888.2889.2891.2893.2894.2895.2897.2898.2900.2901.2908.2909.2913.2914.2916.2917.2918.2919.2920.2922.2923.2927.2929.2930.2931.2940.2941.2947.2949.2950.2956.2958.2961.2963.2964.2965.2966.2968.2973.2975.2979.2980.2981.2983.2985.2986.2987.2994.2995.2997.2999.3000.3002.3003.3005.3008.3009.3010.3012.3016.3017.3018.3019.3024.3025.3028.3034.3037.3038.3043.3048.3052.3053.3055.3058.3059.3063.3066.3068.3070.3073.3074.3075.3076.3077.3078.3089.3090.3093.3094.3095.3097.3099.3104.3106.3109.3112.3117.3119.3126.3127.3128.3130.3135.3136.3145.3150.3151.3154.3155.3163.3167.3172.3173.3182.3183.3184.3185.3187.3188.3189.3190.3194.3196.3209.3210.3211.3214.3215.3217.3219.3222.3223.3225.3226.3227.3228.3230.3231.3234.3235.3236.3237.3238.3240.3244.3245.3250.3251.3253.3257.3260.3268.3270.3272.3281.3288.3290.3292.3293.3295.3296.3299.3300.3306.3307.3314.3315.3316.3318.3324.3327.3328.3330.3331.3531.3731.3831.3931.4131.4531.4631.4731.4831.5031.5231.6931.7031.7235.7831.7931.8931.9731.10231.10631.11031.11531.12831.13632; usprivacy=1YNN; _imntz_error=0; editionPostpone=1695904428925; gtmFired=OK; g_state={"i_p":1695911666208,"i_l":1}; r_p_s_n=1; adsFreeSalePopUp=3; connectId={"lastUsed":1695904544235,"lastSynced":1695904544235}; _cc_id=a8848c7c36356486a869d187657dcb80; panoramaId_expiry=1695990944268; panoramaId=7276961a789524cd91d5264f8549a9fb927a5c09636c5c3a44d6d6de0d6c8174; panoramaIdType=panoDevice; cto_bundle=gE_40l9KcmJNZ1ltSlhIRGxrZmRBMUkxaVllQ1hETHNwQnNJVVBlQzFpMEJHU1lIbVFFenVYbUwwRjlSN0xGVTVmNWRQVmZTa2RJbHY4OFQxNjk3VFNTNEZLY0J0aVBiamRRb1VqaWZobmZoTDE3U045Y1FtVk1XRkhvNTdZRjh4UkJxQWNBOUdYS3BNZ21HbXA0Q2JtNG8yYmExeW04SXI1S3N5ZTloenlSa2NZbHJQVSUyQnliS2VVZWxCdkdCcjV4SmU4bTRXMXNUWXFrMUJBMFZxQTYlMkZHRDJIUSUzRCUzRA; nyxDorf=YmZjNDJnNXdjNGFqNWFjf2IyN21iZzomMDBhYzYx; page_view_count=5; invpc=5; _ga=GA1.1.1499573541.1695904425; _ga_C4NDLGKVMK=GS1.1.1695904424.1.1.1695905631.44.0.0; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Sep+28+2023+14%3A53%3A51+GMT%2B0200+(Central+European+Summer+Time)&version=202303.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=844e0ccc-65b9-4e27-b898-b92b1fe5aa82&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CSTACK42%3A1&geolocation=NL%3BZH&AwaitingReconsent=false; _gat_allSitesTracker=1',
        'Referer':'https://www.investing.com/stock-split-calendar/',
        'Sec-Ch-Ua':'"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'Sec-Ch-Ua-Platform':"macOS",
        'Sec-Fetch-Dest':'document',
        'Sec-Fetch-Mode':'navigate',
        'Sec-Fetch-Site':'same-origin',
        'Sec-Fetch-User':'?1',
        'Upgrade-Insecure-Requests':'1'
    }   
    url = f'https://www.investing.com/equities/{code}'
    r = scraper.get(url, headers=headers,timeout=30)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    exchange = soup.select("span.text-xs\/5")
    exchange = None if exchange == [] else exchange[0].get_text()
    pre_close = soup.select("dt:contains('Prev. Close') + .font-semibold span:nth-of-type(2)")
    pre_close = None if pre_close == [] else pre_close[0].string
    isin = soup.select("dt:contains('ISIN') + dd")
    isin = None if isin == [] else isin[0].get_text().strip()
    details = [exchange, isin, pre_close] 
    return details

def run_fetch_details(code):
    attempts = 0
    while attempts < 3:
        try:
            df = get_stock_details(code)
            break
        except Exception as e:
            attempts += 1
            print(f'{e}, refetching: {code}')
    return df


def summarize():
    divident_df = get_today_calendar(event='dividends')
    split_df = get_today_calendar(event='stock-split')
    df = divident_df.merge(split_df, how='outer', on=['href','country','symbol'])
    df['details'] = df['href'].progress_apply(run_fetch_details)
    df[['exchange','isin','pre_close']] = pd.DataFrame(df['details'].tolist(), index= df.index)
    df = df [['isin','exchange','symbol','href','country','type','dividend','split_ratio','pre_close']]
    return df


def update_result(df):
    df.to_csv(save_path, index = False, header=True, encoding = 'utf-8') 


 
# 后复权计算股价涨幅
if __name__ == '__main__':

    df = summarize()
    update_result(df)
    # print(df)