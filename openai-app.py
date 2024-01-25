# from bardapi import BardCookies

# cookie_dict = {
#     "__Secure-1PSID": "fQjUclNK0M8J0OnAZeG9rxesJr2tb3crYkS8caWF90ZGbnLiFuBARNdaB-RUOdEIZcjYbQ.",
#     "__Secure-1PSIDTS": "sidts-CjIBPVxjStK_knQkbMZkI2h4P_pNX_YmY_U8XX2y0mQUa9P6OLapMlWdj9DJ88ngPCiytRAA",
#     "__Secure-1PSIDCC": "ABTWhQHXsEB_cp3mdEYPSKjdBzgPFjJbl7ZXojGDZz5zDr_X2lM9doEVM9cDQQLvWLsCmBTHwRs"
#     }

# bard = BardCookies(cookie_dict=cookie_dict)
# print(bard.get_answer("你好，特变电工最新信息")['content'])



from gpt4_openai import GPT4OpenAI


my_session_token = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..cSSNdH8pYvcyfqN-.yXRBu2YwHRGSjhyJgUaKdGocx9_QmMK3dPo-r2iBu2S73HdxOFuboVXvgVFH2K4BFW61xCEVVr3Me5O2YABX_YQnvbIlSXtLto2M9jzNTDnqL8znm8-WH8nOCO4q14AILciGZUgisL0i1xftc-0T6xBPpXL4PmZPRUAJd85Hb7sGS1gSyQNu2UCpbmEohMVVLl-yuEB8jiOP4IzBqoTSpmDbylE57cVK_jF5nTy7UtA8c_2YdaFy-yq-_w1ZGdJKls4m8DUrBPqsvxtVGaFQ-bbkwkTpFExeaSDPND8vCJp8FhzMN1Ux-eSeiAc1kCFkNDDou7A60Rth4rWihLnxlRJL5M_vkNuBMGUY0lY8X28CLXuTYgA9XR01gSnMDqk4uePgI_S1ayxEpK4LqRfVRP9cRK7qj8Ns5Ee8GMuZNCzravsdbN2IURQ-FmQB--ulSUcJZsBcsvNf1sZFD5LqX_DDh3AfGsOWxnLQ-WsSdXOoM5GStvvDZXeAMxKRZUc3_Xov7s3Tef7KKK4-XqQqfwLBEQtLEZgIALmRkiEDTR6UQPE9Isre7VTnwG2TIh9XpqYLUY0TPDeWqhv5QLrYZw_JnHktLid8f07H0OKEfvF94gWr8hr1oNCpycc_bsLYcjb7NUoqMJG5N1hsDrgGvUaBLA-bCQqYpc9pLhndMbdfCX5k9_jLgI0UJMOrxfnK8xt67qelcL3QAzM4JKGyyIC5FTYUmh1i6t-5RjnqWaMEp6Wg_blokXTYLWqPzyQ9ET_b2pMe9S4MPyQSE1343mor38y21cEr44TA06Y5OEgll-gtTolYh_73dEMEsZ3D7-HmXEKyqFN9GJ8y7tBHtgIcG5i-92M6gOd302IolvYc5EYlzGkwyBmZLOj2plesm2xB3Jfn4sVmhQSiT76SLGeqLHjDEaAUj10S_6IYgwKZMJocRIzZQ_8pG79fdFbn1S4E52MUkoy8-UvIB4wVumDTAXCHFbxYrmolCVRx5B8FHmcAKhXUCkxiREPq3SqwFbrIYgadU22Ibd--lkwmir7UHyVzPoYPBboJ4c-nuYN_4OUAaZunicLmkCw6ecyFeyVdgqDLCCX9KZayc6j8ixPX5Iovf74Lk2kzJldRh5IOy3W46MtjNDsUIWCi9EQdl0ox1SgPf4VmFrxfJPb9UdNb4VIk-OQb5nId_uG-MtNr537IUJi1grDlVtiiAy8-RQ7irrAtcTzrEelzd77RT3PtTa68LYGUtW6FWbqbntAqPtWaVZEj-6c03IGpytHqTBSV5SJK3BGbOWHlFmM-SRNDW0SHOj7KGgVeWRJsl81P0kJ38pnID5eCFVhboH4SIG5mySOldYxSxl4Xtpuf92LE0CqnyytLaOHB3vHq9sJfEMbkZyOEJL3l5AwqTGXIf_6e6yAXeM4QD_gzC3elh1dUlCzbzi3x2HA70oei5LbwvU1fe24aDCh7G3zzWzX1BzLL6uIcicfSCVuYbCvhFZ9JDZ8YjAhWlzCP6NGnr0X-9leN_VawOwNzZJKwT7fdv9bm2FBxxvy0rILLkM9hFPzfCF5Xg11t7Wf1x56jowdAjRq8z4ViXpoP-v6u-6HWeQs9NenleceKfMc7qWwTE6c3GwsEEAWQH8jSSOqiRarxCAb5f3ndjTW6ngXAHPXZQXXl2T9PZTm1TEUYjSUzIC6a0gIajcU5-LyvWvbM0j2I_FTfWCCTkDyIG977Lxj1asvAwYWk6x27W_YXaC_zqEOE-IBG-dIyLhWvoDSBypSNnrwhmbnQKbY9ubg_ee77RJH2X9pQri6KEvW1lWsUMksNJ8jKw-LWMgSxK4ZVzuWtW_SBFLhfBrXscHLYSQKwbSFiDU13QsrEz3chL_jgs9d329QKl3xjNlhPPHzxnywskrr4OyAfRd_EKuz5DdeVZTmhGog85NJDA9DZab1taiNfD4xpmjyDAUywUnTKJ3TJLuSzJDjpT7hgkpUJ6O3VtOn5-1Kk52gsbytcvPDxpftIdSYXEWxUNrlrT8dXV-1P_I_vq149dqS3ANhHxkGrnmvL-yLw1bRld7wUrmGEDe5OhmmhtoqV6KJLqI5f-Cf2B92u-y0tRm8XlbVaGTvsAMXZfECkyiwt4hP_Aw0lvA-audFJs_F0zrttTz_TuBnOnQYRrfX-CkWIWk1LInvtbADgKPccj1eujQzpInRz_-byDzCsx8hGpvuXRS_jx7kscalZe6gNV7glvMBecg0wOL5fqRNPbSx3FKlSAchOsoIalS4AZOFhQ1bVf_jTFMB4dCJvm5WtvsTuiMK7Tg94lp4XmlnodW6XHmXJlhGzStgD0wBQbNbwJlxIG03Y6oIhKPDAKqEdX8g8eJ34AkNvEwIpMJk_kfu94yIm-cx29snR2enKuN_kQ82ve9_uj9g5efofhElrzPocc-O_x4CsxCqIfpjtXWF8JlwkkBn0CthNnVro85JJDDp2G8yVZ40DnZoddswcqsUwwjf0hTvUde8bYubq9X2r9-uZiTD3ZRNlidoQZnHp21Vb5TiDksGwejWEIctxHNRe2kU5hU97P4bISYV--mOyuCFSZNI_hIyqcaWDlZskqwbmw8ZBCqHjHiFr3w1stqQR4nvkDa481sOWKhsZDLGUL3bz5A5FHE6sVFlxiQlBTbfu1fUtTvS2MbF_7sdiHx5M1fhkHVqutoWcgaSI1vehUaNJc_r4fsclGyrYHK5MMJ7QEYdlin0Ci8luT9SwKl7BkJV3LCrlxYdJ_9m0IFTiNvSvpppD1jqcphHj3PNnU2NHiQaC5wKb0eI.NxN7h22J1PPtlHv5jTMMOA'
# Token is the __Secure-next-auth.session-token from chat.openai.com
llm = GPT4OpenAI(token=my_session_token, headless=True, model='gpt-3.5')
# GPT3.5 will answer 8, while GPT4 should be smart enough to answer 10
response = llm('If there are 10 books in a room and I read 2, how many books are still in the room?')
print(response)