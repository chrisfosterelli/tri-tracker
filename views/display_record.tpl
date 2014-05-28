<!DOCTYPE html>
<html>
 <head>
  <title>Tri-tracker</title>
  <meta name="viewport" content="width=device-width; initial-scale=1.0; maximum-scale=1.0; user-scalable=0;" />
  <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.0.2/css/bootstrap.min.css" />
  <link rel="stylesheet" href="/static/tritracker.css" />
 </head>
 <body>
  <h3 class="block">
    Exercise View
  </h3>
  %if best['percentage'] >= 0:
  <h3 class="block green">
    New Record
  </h3>
  %end
  <p class="block white">
    Exercised at a pace of {{'%.2f' % pace}} min/km
  </p>
  <h3 class="block">
    Previous
  </h3>
  <p class="block white">
    %if previous['percentage'] >= 0:
    {{'%.2f' % previous['percentage']}}% faster
    %else:
    {{'%.2f' % previous['percentage']}}% slower
    %end
  </p>
  <p class="block white">
    %if previous['seconds'] >= 0:
    {{'%.1f' % previous['seconds']}} seconds faster
    %else:
    {{'%.1f' % previous['seconds']}} seconds slower
    %end
  </p>
  <h3 class="block">
    Average
  </h3>
  <p class="block white">
    -
  </p>
  <p class="block white">
    -
  </p>
  <h3 class="block">
    Previous Best
  </h3>
  <p class="block white">
    %if best['percentage'] >= 0:
    {{'%.2f' % best['percentage']}}% faster
    %else:
    {{'%.2f' % best['percentage']}}% slower
    %end
  </p>
  <p class="block white">
    %if best['seconds'] >= 0:
    {{'%.1f' % best['seconds']}} seconds faster
    %else:
    {{'%.1f' % best['seconds']}} seconds slower
    %end
  </p>
  <h3 class="block">
    Information
  </h3>
  <p class="block white">
    Total time of {{time}}
  </p>
  <p class="block white">
    Distance covered was {{distance}}
  </p>
  <p class="block white">
    Occured on {{date.strftime('%B %d, %Y')}}
  </p>
  <p class="block white">
    Activity was a {{type}}
  </p>
 </body>
</html>
