#!/bin/bash

echo -e "<DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0 Transitional//EN\">\n\
<html>\n<head>\n<title>Fret's Home</title>\n<!--meta http-equiv=\"REFRESH\" \
content=\"0;url=http://\
$(dig +short myip.opendns.com @resolver1.opendns.com)\"-->\n</head>\n\
<body>$(dig +short myip.opendns.com @resolver1.opendns.com)\
</body>\n</html>\n"
