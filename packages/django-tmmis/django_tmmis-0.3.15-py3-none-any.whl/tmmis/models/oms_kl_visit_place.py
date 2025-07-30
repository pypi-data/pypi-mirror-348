from .base_model import *


class OmsKlVisitPlace(BaseModel):
    id = models.AutoField(db_column="kl_VisitPlaceID", primary_key=True)
    code = models.CharField(db_column="Code", max_length=50, default="не определено")
    name = models.CharField(db_column="Name", max_length=255, default="не определено")
    date_b = models.DateTimeField(db_column="Date_B", default="1900-01-01")
    date_e = models.DateTimeField(db_column="Date_E", default="2222-01-01")
    code_egisz = models.CharField(db_column="CodeEGISZ", max_length=50, default="")
    name_egisz = models.CharField(db_column="NameEGISZ", max_length=255, default="")
    is_tap = models.BooleanField(db_column="IsTAP", default=False)
    guid = models.CharField(db_column="VisitPlaceGUID", max_length=36, default=uuid4)

    class Meta:
        managed = False
        db_table = "oms_kl_VisitPlace"
