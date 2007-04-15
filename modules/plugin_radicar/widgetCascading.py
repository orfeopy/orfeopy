#!/usr/bin/env python 
# coding: utf8 
from gluon.html import *
from gluon.http import *
from gluon.validators import *
from gluon.sqlhtml import *
import uuid
# request, response, session, cache, T, db(s) 
# must be passed and cannot be imported!

"""
   web2py widgets
   A collection of user interface widgets for web2py
   Developed by Nathan Freeze
   Copyright 2010 nathan@freezable.com
   License: GPLv2
"""

class CascadingSelect(object):
    """
       Creates dependent selects based on table relationships.
       Pass the tables in order of least to most specific
       Based on http://web2pyslices.com/main/slices/take_slice/85
    """
    def __init__(self, *tables):
        self.tables = tables 
        self.prompt = lambda table:str(table)   
        
    def widget(self,f,v):
        uid = str(uuid.uuid4())[:8]
        d_id = "cascade-" + uid
        wrapper = TABLE(_id=d_id)
        parent = None; parent_format = None; 
        fn =  '' 
        vr = 'var dd%s = [];var oi%s = [];\n' % (uid,uid)
        prompt = [self.prompt(table) for table in self.tables]
        vr += 'var pr%s = ["' % uid + '","'.join([str(p) for p in prompt]) + '"];\n' 
        f_inp = SQLFORM.widgets.string.widget(f,v)
        f_id = f_inp['_id']
        f_inp['_type'] = "hidden"
        for tc, table in enumerate(self.tables):             
            db = table._db     
            format = table._format            
            options = db(table['id']>0).select()
            id = str(table) + '_' + format[2:-2]             
            opts = [OPTION(format % opt,_value=opt.id,
                                 _parent=opt[str(parent)] if parent else '0') \
                                  for opt in options]
            opts.insert(0, OPTION(prompt[tc],_value=0))
            inp = SELECT(opts ,_parent=str(parent) + \
                                  "_" + str(parent_format),
                                  _id=id,_name=id,
                                  _disabled="disabled" if parent else None)
            wrapper.append(TR(inp))
            next = str(tc + 1)
            vr += 'var p%s = jQuery("#%s #%s"); dd%s.push(p%s);\n' % (tc,d_id,id,uid,tc)            
            vr += 'var i%s = jQuery("option",p%s).clone(); oi%s.push(i%s);\n' % (tc,tc,uid,tc)
            fn_in = 'for (i=%s;i<%s;i+=1){dd%s[i].find("option").remove();'\
                    'dd%s[i].append(\'<option value="0">\' + pr%s[i] + \'</option>\');'\
                    'dd%s[i].attr("disabled","disabled");}\n' % \
                           (next,len(self.tables),uid,uid,uid,uid)
            fn_in +='oi%s[%s].each(function(i){'\
                    'if (jQuery(this).attr("parent") == dd%s[%s].val()){'\
                    'dd%s[%s].append(this);}});' % (uid,next,uid,tc,uid,next)            
            fn_in += 'dd%s[%s].removeAttr("disabled");\n' % (uid,next)
            fn_in += 'jQuery("#%s").val("");' % f_id
            if (tc < len(self.tables)-1):
                fn += 'dd%s[%s].change(function(){%s});\n' % (uid,tc,fn_in) 
            else:
                fn_in = 'jQuery("#%s").val(jQuery(this).val());' % f_id
                fn += 'dd%s[%s].change(function(){%s});\n' % (uid,tc,fn_in)
                if v:
                    fn += 'dd%s[%s].val(%s);' % (uid,tc,v)                       
            parent = table
            parent_format = format[2:-2]

        wrapper.append(f_inp)
        wrapper.append(SCRIPT(vr,fn))
        return wrapper
