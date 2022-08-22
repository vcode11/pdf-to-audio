from PyPDF2 import PdfReader
from io import BytesIO
from gtts import gTTS

def getPDFContentDict(pdfReader: PdfReader):
    outline = pdfReader.getOutlines()
    table_of_contents = []
    for outline_item in outline:
        title = outline_item.title
        indirect_page_ref = outline_item.page 
        page_number = pdfReader._get_page_number_by_indirect(
            indirect_page_ref
            )
        table_of_contents.append((page_number,title))
    return table_of_contents

def getAudioFileContent(pdfReader, table_of_contents):
    audioFilesDict = {}
    i = 0
    for page_number in range(1,pdfReader.getNumPages()):
        if i+1 != len(table_of_contents) and table_of_contents[i+1][0] <= page_number:
            i+=1
        audioFilesDict.setdefault((table_of_contents[i][1], i), '')
        text = pdfReader.getPage(page_number).extractText()
        audioFilesDict[(table_of_contents[i][1], i)]+= text
    return audioFilesDict

def createAudioFiles(audioFilesDict):
    for title_index_tuple, text in audioFilesDict.items():
        if text == '':
            continue
        print(f"writing {title_index_tuple}")
        tts = gTTS(text)
        tts.save(str(title_index_tuple[1] + 1) + '' + title_index_tuple[0] + ".mp3")

def main():
    pdfFileName = 'Zero to One.pdf'
    with open(pdfFileName, "rb"):
        pdfReader = PdfReader(pdfFileName)
        contents = getPDFContentDict(pdfReader)
        audioFileContents = getAudioFileContent(pdfReader, contents)
        createAudioFiles(audioFileContents)

if __name__ == '__main__':
    main()
