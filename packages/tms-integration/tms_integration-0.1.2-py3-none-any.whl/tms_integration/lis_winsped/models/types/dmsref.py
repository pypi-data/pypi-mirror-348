from pydantic import BaseModel, Field
from typing import Literal, Optional


class DmsRef(BaseModel):
    satzart: Literal["DMSREF"] = "DMSREF"
    referenz: str
    dmsdoknr: int
    dmsrefnr: int
    aufnr: int
    kundennr: Optional[str]
    liefnr: Optional[str]
    refnr: Optional[str]
    kommnr: Optional[str]
