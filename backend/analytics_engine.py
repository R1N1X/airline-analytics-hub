def get_top_routes(flights, top_n=10):
    from collections import Counter
    routes = [f"{f['origin']} → {f['destination']}" for f in flights]
    most_common = Counter(routes).most_common(top_n)
    return [{"route": route, "count": count} for route, count in most_common]

def get_airline_distribution(flights):
    from collections import Counter
    airlines = [f["airline"] for f in flights]
    return dict(Counter(airlines))

def get_price_stats(flights):
    prices = [f["price"] for f in flights if "price" in f]
    return {
        "avg_price": round(sum(prices) / len(prices), 2) if prices else 0,
        "min_price": min(prices) if prices else 0,
        "max_price": max(prices) if prices else 0
    }
