"""to create package you have to have __.init__.py in that folder,
it tells python that this is package"""

# import from main package
from MainPackage import some_main_script
# import from sub package, just have to use "."
from MainPackage.SubPackage import some_sub_script
# import func
from MainPackage.SubPackage.some_sub_script import sub_report

some_main_script.main_report()
some_sub_script.sub_report()
sub_report()