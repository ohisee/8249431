#
# Apply rot 13 handler extends base handler
#

from basehandler import BaseHandler;
from rot13 import applyRot13;

'''
/unit2/rot13
'''
class ApplyRot13Handler(BaseHandler):
    def get(self):
        self.render("rot13-form.html");
        
    def post(self):
        textdata = self.request.get("text");
        #self.response.write(form % {'value': applyRot13(textdata)});
        textdatarot13 = applyRot13(textdata);
        self.render("rot13-form.html", text = textdatarot13);