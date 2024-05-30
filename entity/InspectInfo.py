from datetime import datetime


class InspectInfo:
    def __init__(self):
        self.info_id: int | None = None
        self.name: str | None = None
        self.identity: str | None = None
        self.inspect_time: datetime | None = None
        self.age: int | None = None
        self.height: float | None = None
        self.height_assess: str | None = None
        self.weight: float | None = None
        self.weight_assess: str | None = None
        self.bmi: float | None = None
        self.bmi_assess: str | None = None
        self.eye_sight_l: float | None = None
        self.eye_sight_r: float | None = None
        self.eye_sight_assess: list[str] | None = None
        self.sph_l: float | None = None
        self.sph_r: float | None = None
        self.cyl_l: float | None = None
        self.cyl_r: float | None = None
        self.axis_l: int | None = None
        self.axis_r: int | None = None
        self.tooth_num: int | None = None
        self.decayed_tooth_num: int | None = None
        self.oral_ills: list[str] | None = None
        self.hb: float | None = None
        self.hb_assess: str | None = None
        self.other: list[str] | None = None
        self.spirit: list[str] | None = None
        self.status: int | None = None
        self.upload_message: str | None = None
        self.spirit_ill: list[str] | None = None
        self.eye_ills: list[str] | None = None
