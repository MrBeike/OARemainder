import win32com.client as wc

# app = wc.Dispatch('wps.Application')
# app = wc.Dispatch("Word.Application")
# app = wc.gencache.EnsureDispatch('kwps.application')
app = wc.Dispatch('Wps.Application')

doc = app.Documents.Add()
app.Visible = 1
# doc = word.Documents.Open('1.docx')WPS