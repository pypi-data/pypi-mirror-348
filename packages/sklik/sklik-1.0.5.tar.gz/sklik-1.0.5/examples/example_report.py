import sklik
from sklik.object import Account

token = "<sklik_token>"
sklik.SklikApi.init(token)

account_id = int("<account_id>")
account = Account(account_id)

service = "campaigns"  # "groups", "ads", "keywords"
since = "2025-01-01"
until = "2025-01-31"
fields = ["id", "name", "status", "impressions", "clicks", "totalMoney"]
granularity = "daily"  # "weekly", "monthly", "quarterly", "yearly", "total"

report = sklik.create_report(
    account,
    service,
    fields,
    since,
    until,
    granularity
)

for item in report:
    print(item)
