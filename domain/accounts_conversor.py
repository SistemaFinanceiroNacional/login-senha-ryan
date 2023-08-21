from domain.commontypes.types import AccountId, LedgerId, LedgerType

STAGE_DIGIT = LedgerType.STAGE
MAIN_DIGIT = LedgerType.MAIN
DRAFT_DIGIT = LedgerType.DRAFT


def get_stage_id(bank_acc_id: AccountId) -> LedgerId:
    return LedgerId(bank_acc_id, STAGE_DIGIT)

def get_main_id(bank_acc_id: AccountId) -> LedgerId:
    return LedgerId(bank_acc_id, MAIN_DIGIT)

def get_draft_id(bank_acc_id: AccountId) -> LedgerId:
    return LedgerId(bank_acc_id, DRAFT_DIGIT)
