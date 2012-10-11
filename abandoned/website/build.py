=======
Website
=======

:date: 2012-07
:author: Curtis Sand

- Modify ``pyLib.rst.toHtml`` to capture stderr and log it properly
  using the ``logging`` module.
- Builder should handle writing output files that exist by creating a
  sub-dir in the config.buildDir, writing the file to a 'staging'
  directory.  At the end of the build process, generate a staging area
  page.
- Builder should call a "page parser controller" that will control
  which source files go to which "page parser". (page parser ideas:
  blog, reference, note, photoGallery, etc.)
