<!DOCTYPE html>
<html>
 <head>
  <title>Tri-tracker</title>
  <meta name="viewport" content="width=device-width; initial-scale=1.0; maximum-scale=1.0; user-scalable=0;" />
  <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.0.2/css/bootstrap.min.css" />
  <link rel="stylesheet" href="/static/tritracker.css" />
 </head>
 <body>
  <p class="block">
    %if days_since_last_entry:
    The last time you trained was {{days_since_last_entry}} days ago.
    %else:
    You have already trained today.
    %end
  </p>
  <form method="post" action="/record">
   <input type="text" name="time" class="block form-control" placeholder="Enter time" />
   <input type="text" name="distance" class="block form-control" placeholder="Enter distance" />
   <select name="type" class="block form-control">
    <option value="jog">Jog</option>
    <option value="bike">Bike</option>
    <option value="swim">Swim</option>
   </select>
   <input type="submit" class="block btn btn-primary form-control" value="Create Log" />
  </form>
 </body>
</html>
