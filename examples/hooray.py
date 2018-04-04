import tgflow
key='539066078:AAHCUsr8ZoP9JtP5KqOMuL7f_UoFyyH6wik'

tgflow.configure(token=key,state='start')
tgflow.start({'start':{
    'text':tgflow.paste("Hello, i'm hooray bot. Hooray %i times!",
                   'count',default=1),
    'buttons':[{
        'Say hooray':lambda count=1:
        ('start',{'count':count+1})
    }]
}
})
