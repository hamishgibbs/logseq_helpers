import sys
from datetime import datetime
from datetime import timedelta
import os
from dotenv import load_dotenv

def get_weekly_dates(date):
    weekly_dates = []
    for i in range(7):
        weekly_dates.append(date + timedelta(days=i))
    return weekly_dates

def custom_strftime(format, t):
    def nth(d):
        return "%d%s" % (d, "th" if 4<=d<=20 else {1:"st",2:"nd",3:"rd"}.get(d%10, "th"))
    return t.strftime(format).replace("{th}", nth(t.day))

def get_weekly_plan_template(date):
    page_embeds = []
    page_embeds.append("""TODO Set up new daily plan templates
TODO Migrate previous week's plan
TODO Check calendar for events this week
TODO Read outstanding emails""")

    for date in get_weekly_dates(date):
        page_embeds.append(f"{{{{embed [[{custom_strftime('%b {th}, %Y', date)}]]}}}}")
    
    return page_embeds

def get_daily_plan_template(date):
    return [
        "#### Major Items", 
        """#+BEGIN_QUERY
{:title [:h4 "Scheduled"]
 :query [:find (pull ?b [*])
   :in $ ?day  ;
   :where
     [?b :block/scheduled ?d]  ;
     [(= ?d ?day)]  ;
 ]
 :inputs [""" + f"{date.strftime('%Y%m%d')}" + """]  ;
 :table-view? false
}
#+END_QUERY""",
        """#+BEGIN_QUERY
{:title [:h4 "Deadlines"]
 :query [:find (pull ?b [*])
   :in $ ?day  ;
   :where
     [?b :block/deadline ?d]  ;
     [(= ?d ?day)]  ;
 ]
 :inputs [""" + f"{date.strftime('%Y%m%d')}" + """]  ;
 :table-view? false
}
#+END_QUERY""",
        "#### Other Items", 
        "#### Notes"]

def ordinal(n):
    """Return the ordinal number string of n, for example 1 -> 1st, 2 -> 2nd."""
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return str(n) + suffix

def format_date_with_ordinal(date):
    """Return the formatted date with the day having the appropriate ordinal suffix."""
    day_with_ordinal = ordinal(date.day)
    return date.strftime(f'%b {day_with_ordinal}, %Y')

def compute_monday(date):
    """Return the Monday of the week for the given date."""
    return date - timedelta(days=date.weekday())

def main():
    load_dotenv()
    logseq_path = os.getenv("LOGSEQ_GRAPH_PATH")
    if not logseq_path:
        raise Exception("LOGSEQ_GRAPH_PATH is not set in .env file")

    user_date = datetime.today()
    monday_date = compute_monday(user_date)
    
    weekly_plan_fn = f"{logseq_path}/pages/Weekly Plan {format_date_with_ordinal(monday_date)}.md"
    print(weekly_plan_fn)
    with open(weekly_plan_fn, "a") as f:
        f.write("\n".join(get_weekly_plan_template(monday_date)))
    print('✅ Created Weekly Plan')

    for date in get_weekly_dates(monday_date):
        day_journal_fn = f"{logseq_path}/journals/{date.strftime('%Y_%m_%d')}.md"
        with open(day_journal_fn, "a") as f:
            f.write("\n".join(get_daily_plan_template(date)))
        print(f'✅ Created Daily Plan for {date.strftime("%b %d, %Y")}')

if __name__ == "__main__":
    main()
