"""
This File consists of url sampler for scan thread.
"""


class sampler:
    callTimes = 0

    def __init__(self):
        pass

    @staticmethod
    def compute_link_order(link):
        link = "/" + link
        order = 0
        flag = 0
        for i in link:
            if i == '/':
                if flag == 0 :
                    order += 1
                    flag = 1
            else:
                flag = 0
        return order - flag + 1

    @staticmethod
    def basic_sampler(sub_urls):
        url_list = list(sub_urls)
        if sampler.callTimes >= len(url_list):
            sampler.callTimes = 0
        idx = sampler.callTimes
        sampler.callTimes += 1
        return url_list[idx]

    @staticmethod
    def geometry_sampler(sub_urls):
        # sample from geometry distribution
        order_dict = {}
        for url in sub_urls:
            url_order = sampler.compute_link_order(url)
            if url_order not in order_dict:
                order_dict[url_order] = [url]
            else:
                order_dict[url_order].append(url)
        orders = sorted(order_dict.keys())
        max_order = orders[-1]
        upper_bound = 0
        for i in orders:
            upper_bound += 1 << (max_order - i)
        import random
        vv = random.randint(1, upper_bound)
        idx = 0
        for i in orders:
            idx += 1
            vv -= (1 << (max_order - i))
            if vv <= 0:
                idx -= 1
                break
        vvorder = orders[idx]
        return random.choice(order_dict[vvorder])
