from nostr_agents.nwc import processNWCstring, tryToPayInvoice, listTx, getBalance, didPaymentSucceed, makeInvoice, checkInvoice
from bolt11.decode import decode
import time


class NWCClient(object):
    def __init__(self, nwc_str: str):
        self.nwc_info = processNWCstring(nwc_str)

    def list_tx(self) -> list:
        return listTx(self.nwc_info)['result']['transactions']

    def get_balance(self) -> int:
        return getBalance(self.nwc_info)['result']['balance']

    def make_invoice(self, amt: int = None, desc: str = None) -> str:
        return makeInvoice(self.nwc_info, amt=amt, desc=desc)['result']['invoice']

    def check_invoice(self, invoice: str = None, payment_hash: str = None) -> dict:
        return checkInvoice(self.nwc_info, invoice=invoice, payment_hash=payment_hash)

    def did_payment_succeed(self, invoice: str = None) -> bool | str:
        return didPaymentSucceed(self.nwc_info, invoice=invoice)

    def try_pay_invoice(self, invoice: str, amt: int = None):
        decoded = decode(invoice)
        if decoded.amount_msat and amt:
            if decoded.amount_msat != amt * 1000:  # convert to msats
                raise RuntimeError(f'Amount in invoice [{decoded.amount_msat}] does not match amount provided [{amt}]')
        elif not decoded.amount_msat and not amt:
            raise RuntimeError('No amount provided in invoice and no amount provided to pay')
        tryToPayInvoice(self.nwc_info, invoice=invoice, amnt=amt)

    def on_payment_success(self, invoice: str, callback=None, unsuccess_callback=None, timeout: int = 60, interval: int = 5):
        """
        Listen for payment success for a given invoice.
        :param invoice: The invoice to listen for.
        :param callback: The callback to call on success.
        :param timeout: The timeout in seconds.
        :param interval: The interval in seconds to check for payment success.
        """
        start_time = time.time()
        success = False
        while True:
            if self.did_payment_succeed(invoice):
                success = True
                if callback:
                    callback()
                break
            if time.time() - start_time > timeout:
                break
            time.sleep(interval)
        if not success:
            if unsuccess_callback:
                unsuccess_callback()
