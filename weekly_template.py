import sys
from datetime import datetime
from datetime import timedelta

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

def main():
    if len(sys.argv) < 2:
        raise Exception("Specify root directory of logseq graph")

    logseq_path = sys.argv[1]

    if len(sys.argv) == 3:
        date = datetime.strptime(sys.argv[2], '%Y-%m-%d')
    else:
        date = datetime.today()
   
    if date.weekday() != 0:
        raise Exception("Starting date must be a Monday")
    
    weekly_plan_fn = f"{logseq_path}/pages/Weekly Plan {format_date_with_ordinal(date)}.md"
    print(weekly_plan_fn)
    with open(weekly_plan_fn, "a") as f:
        f.write("\n".join(get_weekly_plan_template(date)))
    print('✅ Created Weekly Plan')

    for date in get_weekly_dates(date):
        day_journal_fn = f"{logseq_path}/journals/{date.strftime('%Y_%m_%d')}.md"
        with open(day_journal_fn, "a") as f:
            f.write("\n".join(get_daily_plan_template(date)))
        print(f'✅ Created Daily Plan for {date.strftime("%b %d, %Y")}')

if __name__ == "__main__":
    main()
