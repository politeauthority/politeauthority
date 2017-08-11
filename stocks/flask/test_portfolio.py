from modules import portfolio_event_collections

if __name__ == '__main__':
    portfolio = portfolio_event_collections.get_by_portfolio_id(1)
    print portfolio
