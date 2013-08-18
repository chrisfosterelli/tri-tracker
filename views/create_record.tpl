<!DOCTYPE html>
<html>
 <head>
  <title>Tri-tracker</title>
 </head>
 <body>
  <p>
   The last time you exercised was {{days_since_last_entry}} days ago.
  </p>
  <form method="post" action="/record">
   <input type="text" name="time" placeholder="Enter time" />
   <input type="text" name="distance" placeholder="Enter distance" />
   <select name="type">
    <option value="jog">Jog</option>
    <option value="bike">Bike</option>
    <option value="swim">Swim</option>
   </select>
   <input type="submit" value="Create" />
  </form>
 </body>
</html>
