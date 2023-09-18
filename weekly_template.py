import sys
from datetime import datetime
from datetime import timedelta

# 1. Create a function called get_weekly_dates that takes in a date and returns a list of dates for the week starting on the given date.
# raise an exception if the starting date isn't a monday

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

def main():
    if len(sys.argv) > 1:
        date = datetime.strptime(sys.argv[1], '%Y-%m-%d')
    else:
        date = datetime.today()
   
    if date.weekday() != 0:
        raise Exception("Starting date must be a Monday")
    
    print("\033[92m>>> WEEKLY PLAN <<<\033[0m")
    print("\n".join(get_weekly_plan_template(date)))
   
    for date in get_weekly_dates(date):
        print(f"\033[92m>>> DAILY PLAN {date.strftime('%Y-%m-%d')} <<<\033[0m")
        print("\n".join(get_daily_plan_template(date)))

if __name__ == "__main__":
    main()
