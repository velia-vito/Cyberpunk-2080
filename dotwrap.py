from typing import List
from math import ceil
from sys import argv


def main():
    """
    Script to auto-text-wrap .dot files
    """

    inFile = argv[1]

    with open(inFile, mode="r", encoding="utf-8") as f:
        text = f.read()

    outText = reformatText(text.replace("\\n", " "), 40, 20, 100)

    with open(inFile, mode="w", encoding="utf-8") as f:
        f.write(outText)


def reformatText(text: str, nodeWidth: int, edgeWidth: int, commentWidth: int) -> str:
    """
    Split labels into roughly equi-sized lines < maxWidth, and comments < commentWidth
    """

    # Split input text into lines
    inLines = text.split("\n")
    outLines = []

    # Process each line
    for line in inLines:

        # Remove initial padding (used only for line type identification)
        sLine = line.strip()

        # If comment, split to commentWidth (note that indent is maintained)
        if sLine.startswith("// "):
            indent, wLine = line.split("// ")

            wSplit = splitLine(wLine, commentWidth - len(indent))

            for each in wSplit:
                outLines.append(indent + "// " + each)

        elif sLine.startswith('label = "'):
            indent, wLine = line.split('label = "')
            wLine = wLine[:-1]  # remove trailing quote

            # Split the line into roughly equal parts based on nodeWidth
            wSplit = splitLine(wLine, len(wLine) // (ceil(len(wLine) / nodeWidth)))

            newLine = indent + 'label = "' + wSplit[0]
            for each in wSplit[1:]:
                newLine += "\\n" + each

            outLines.append(newLine + '"')

        elif sLine.startswith("xlabel = "):
            indent, wLine = line.split('xlabel = "')
            wLine = wLine[:-1]  # remove trailing quote

            # Split the line into roughly equal parts based on nodeWidth
            wSplit = splitLine(wLine, len(wLine) // (ceil(len(wLine) / nodeWidth)))

            newLine = indent + 'xlabel = "' + wSplit[0]
            for each in wSplit[1:]:
                newLine += "\\n" + each

            outLines.append(newLine + '"')

        elif "->" in sLine and '[xlabel = "' in sLine:
            edge, wLine = line.split('[xlabel = "')
            wLine = wLine[:-2]  # remove trailing quote and bracket

            # Split the line into parts based on edgeWidth
            wSplit = splitLine(wLine, edgeWidth)

            newLine = edge + '[xlabel = "' + wSplit[0]
            for each in wSplit[1:]:
                newLine += "\\n" + each

            outLines.append(newLine + '"]')

        else:
            outLines.append(line)

    return "\n".join(outLines)


def splitLine(text: str, width: int) -> List[str]:
    cText = text
    sLines = []

    # Split the text into lines of specified width
    while len(text) > width:
        splitIndex = findPrevSpace(text, width)
        sLines.append(text[:splitIndex])
        text = text[splitIndex + 1 :]

    # If the last line is too short, redistribute the text
    if len(text) < width // 2 and len(sLines) > 0:
        sLines = splitLine(cText, width + (len(text) // len(sLines) + 1))
    else:
        sLines.append(text)

    return sLines


def findPrevSpace(text: str, index: int) -> int:
    # Find the previous space character before the specified index
    for i in range(index, 0, -1):
        if text[i] == " ":
            return i
    return -1


main()
