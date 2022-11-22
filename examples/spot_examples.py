import os, sys, time
import logging
import logging.config
from dotenv import dotenv_values
from datetime import datetime

try:
    from kraken.spot.client import User, Market, Trade, Funding, Staking
except:
    print('USING LOCAL MODULE')
    sys.path.append('/Users/benjamin/repositories/Trading/python-kraken-sdk')
    from kraken.spot.client import User, Market, Trade, Funding, Staking

logging.basicConfig(
    format='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    filemode='w',
    level=logging.INFO
)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)


key = dotenv_values('.env')['API_KEY']
secret = dotenv_values('.env')['SECRET_KEY']

#  _   _  ___ _____ _____
# | \ | |/ _ \_   _| ____|_
# |  \| | | | || | |  _| (_)
# | |\  | |_| || | | |___ _
# |_| \_|\___/ |_| |_____(_)
# ----> More examples can be found in kraken/tests
# examples may not be updated regularily

def user_examples() -> None:
    user = User(key=key, secret=secret)

    print(user.get_account_balance())
    print(user.get_trade_balance())#asset='BTC'
    print(user.get_open_orders())
    print(user.get_closed_orders())
    print(user.get_orders_info(txid='OBQFM7-JNVKS-H3ULEH')) # or txid='id1,id2,id3' or txid=['id1','id2']
    print(user.get_trades_history())
    time.sleep(3)
    print(user.get_trades_info(txid='TCNTTR-QBEVO-E5H5UK'))
    print(user.get_open_positions())#txid='someid'
    print(user.get_ledgers_info())#asset='BTC' or asset='BTC,EUR' or asset=['BTC','EUR']
    print(user.get_ledgers(id='LIORGR-33NXH-LBUS5Z'))
    print(user.get_trade_volume())#pair='BTC/EUR'

    # ____export_report____
    r = user.request_export_report(report='ledgers', description='myLedgers1', format='CSV') #report='trades'
    print(user.get_export_report_status(report='ledgers'))

    # save report to file
    response_data = user.retrieve_export(id_=r['id'])
    handle = open('myexport.zip', 'wb')
    for chunk in response_data.iter_content(chunk_size=512):
        if chunk: handle.write(chunk)
    handle.close()

    print(user.delete_export_report(id_=r['id'], type_='delete'))#type=cancel

def market_examples() -> None:
    market = Market(key=key, secret=secret)

    print(market.get_assets(assets=['XBT']))
    print(market.get_tradable_asset_pair(pair=['DOTEUR']))
    print(market.get_ticker(pair='XBTUSD'))
    print(market.get_ohlc(pair='XBTUSD', interval=5))
    print(market.get_order_book(pair='XBTUSD', count=10))
    print(market.get_recent_trades(pair='XBTUSD'))
    print(market.get_recend_spreads(pair='XBTUSD'))
    print(market.get_system_status())
    time.sleep(2)

def trade_examples() -> None:
    raise ValueError('Attention: Please check if you really want to execute trade functions.')
    trade = Trade(key=key, secret=secret)

    if False:
        print(trade.create_order(
            ordertype='limit',
            side='buy',
            volume=1,
            pair='BTC/EUR',
            price=0.01
        ))
        print(trade.create_order_batch(
            orders=[{
            'close': {
                    'ordertype': 'stop-loss-limit',
                    'price': 120,
                    'price2': 110
                },
                    'ordertype': 'limit',
                    'price': 140,
                    'price2': 130,
                    'timeinforce': 'GTC',
                    'type': 'buy',
                    'userref': '345dsdfddfgdsgdfgsfdsfsdf',
                    'volume': 1000
                },{
                    'ordertype': 'limit',
                    'price': 150,
                    'timeinforce': 'GTC',
                    'type': 'sell',
                    'userref': '1dfgesggwe5t3',
                    'volume': 123
                }
            ],
            pair='BTC/USD',
            validate= false
        ))

        print(trade.edit_order(
            txid='sometxid',
            pair='BTC/EUR',
            volume=4.2,
            price=17000
        ))
        time.sleep(2)

        print(trade.cancel_order(txid='O2JLFP-VYFIW-35ZAAE'))
        print(trade.cancel_all_orders())
        print(trade.cancel_all_orders_after_x(timeout=6))

        # __ not working
    print(trade.cancel_order_batch(orders=['O2JLFP-VYFIW-35ZAAE', 'O523KJ-DO4M2-KAT243', 'OCDIAL-YC66C-DOF7HS', 'OVFPZ2-DA2GV-VBFVVI']))

def funding_examples() -> None:
    raise ValueError('Attention: Please check if you really want to execute funding funtions.')
    funding = Funding(key=key, secret=secret)
    if False:
        print(funding.get_deposit_methods(asset='DOT'))
        print(funding.get_deposit_address(asset='DOT', method='Polkadot'))
        print(funding.get_recend_deposits_status(asset='DOT'))
        print(funding.get_withdrawal_info(asset='DOT', key='MyPolkadotWallet', amount='200'))
        print(funding.withdraw_funds(asset='DOT', key='MyPolkadotWallet', amount=200))
        time.sleep(2)
        print(funding.get_recend_withdraw_status(asset='DOT' ))
        print(funding.cancel_widthdraw(asset='DOT', refid='12345'))
        print(funding.wallet_transfer(asset='ETH', amount=0.100, from_='Spot Wallet', to='Futures Wallet'))

def staking_examples() -> None:
    raise ValueError('Attention: Please check if you really want to execute staking funtions.')
    staking = Staking(key=key, secret=secret)
    if False:
        print(staking.list_stakeable_assets())
        print(staking.list_staking_transactions())
        print(staking.stake_asset(asset='DOT', amount=2000, method='polkadot-staked'))
        print(staking.unstake_asset(asset='DOT', amount=200, method='polkadot-staked'))
        print(staking.get_pending_staking_transactions())
        time.sleep(2)

def main() -> None:
    user_examples()
    market_examples()
    trade_examples()
    funding_examples()
    staking_examples()

if __name__ == '__main__':
    main()