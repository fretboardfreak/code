<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta name="generator" content=
  "HTML Tidy for Linux (vers 7 December 2008), see www.w3.org" />

  <title>Directory File List</title>
  <meta http-equiv="Content-Type" content=
  "text/html; charset=us-ascii" />
  <meta name="generator" content="pandoc" />
  <meta name="author" content="Curtis Sand" />
  <meta name="author" content="Liam Delahunty" />
  <meta name="date" content="July, 2010" />
  <link rel="stylesheet" href=
  "http://curtissand.com/private/pandoc.css" type="text/css" media=
  "all" />
</head>

<body>
  <h1 class="title">Directory File List</h1>

  <div align="center">
  <div id="navcontainer">
  <ul id="navlist">
  <li><a href="../">Parent Directory</a></li>
  </ul>
  </div>

  <?php
  function format_size($size) {
        $sizes = array(" Bytes", " KB", " MB", " GB", " TB", " PB", " EB", " ZB", " YB");
        if ($size == 0) { return('n/a'); } else {
        return (round($size/pow(1024, ($i = floor(log($size, 1024)))), 2) . $sizes[$i]); }
  }

  // open this directory 
  $myDirectory = opendir(".");

  // get each entry
  while($entryName = readdir($myDirectory)) {
          $dirArray[] = $entryName;
  }

  // close directory
  closedir($myDirectory);

  //      count elements in array
  $indexCount     = count($dirArray);
  Print ("$indexCount files<br>\n");

  // sort 'em
  sort($dirArray);

  // print 'em
  print("<TABLE border=1 cellpadding=5 cellspacing=0 class=whitelinks>\n");
  print("<TR><TH>Filename</TH><th>Filetype</th><th>Filesize</th></TR>\n");
  // loop through the array of files and print them all
  for($index=0; $index < $indexCount; $index++) {
          if (substr("$dirArray[$index]", 0, 1) != "."){ // don't list hidden files
                  print("<TR><TD><a href=\"$dirArray[$index]\">$dirArray[$index]</a></td>");
                  print("<td>");
                  print(filetype($dirArray[$index]));
                  print("</td>");
                  print("<td>");
                  print(format_size(filesize($dirArray[$index])));
                  print("</td>");
                  print("</TR>\n");
          }
  }
  print("</TABLE>\n");
  ?>
</body>
</html>
