import sys
import os

from staq.stackSession import StackSession



def test_session_cmd():

    session = StackSession()

    completions = session.getCompletions("")
    assert "pop" in completions

    

# def test_session():

#     session = StackSession()

#     session.parseCommand("int i =42")

#     wordCount = len(session.stack.currentFrame.cells[0].words)
#     wordValue = session.stack.currentFrame.cells[0].words[0].value

#     assert wordCount == 1
#     assert wordValue == 42

# def test_html():
#     session = StackSession()
#     session.stack.baseAddress =0xffffff


#     session.parseCommand('int etc[64]')
#     session.parseCommand('call main(1,"Hello World")')
#     session.parseCommand('char buf[64]')
#     session.parseCommand('call strcpy(buf,argv[0])')
#     session.parseCommand('note 0xfeb3: note on local variable')


#     html = session.stack.toHtml()

#     with open("test.html", "w") as fh:
#         fh.write(html)

# def test_png():
#     session = StackSession()
#     session.stack.baseAddress =0xffffff
#     imagePath = 'test.png'
    
#     session.parseCommand('int etc[64]')
#     session.parseCommand('call main(1,"Hello World")')
#     session.parseCommand('char buf[64]')
#     session.parseCommand('call strcpy(buf,argv[0])')
#     session.parseCommand('note 0xfeb3: note on local variable')


#     session.stack.generatePng(imagePath)

#     assert os.path.exists(imagePath)


if __name__ == "__main__":
    test_session()