# pymusic
Tools for processing music things.

Links
https://muse.dillfrog.com/about/help
https://stackoverflow.com/questions/875476/editing-a-wav-files-using-python
https://www.youtube.com/watch?v=KyP2a0Ms2-c

Think in terms of three layers
    Music
    View
    Engraving

The music layer tracks the notes as object streams
The view maps parts to a score
Engraving deals with fonts, sizes, spacing, etc.

Use a subset of MusicXml notation, define a schema for it.
Create a class that serializes and deserializes in this format.
Use specification defined special character sequences in names to implement part tracking.
Each part should have a stream of notes.

Define each note in terms of frame duration, which can often be a measure, but is just as often more than one measure, especially for any complex meters.
Assume some frame duration M, divide that frame by whole numbers and compare their delta from the actual offset.
Look for the lowest divisor that is closest to determine best match.

# librosa
https://librosa.org/doc/latest/index.html
https://nbviewer.org/github/AllenDowney/ThinkDSP/blob/master/code/scipy2015_demo.ipynb
>py -m pip install librosa
https://github.com/librosa/librosa
https://www.musipedia.org/
https://freesound.org/
https://conference.scipy.org/
https://github.com/AllenDowney/ThinkDSP
https://ismir.net/
>py -m pip install matplotlib
>py -m pip install seaborn
>py -m pip install IPython
>py -m pip install mir_eval

#pyside6
[Qt for Python](https://doc.qt.io/qtforpython-6/index.html)
[Audio Input](https://doc.qt.io/qt-6/qml-qtmultimedia-audioinput.html)
[Audio Output](https://doc.qt.io/qt-6/qml-qtmultimedia-audiooutput.html)
[QML](https://doc.qt.io/qtforpython-6/PySide6/QtQml/index.html#module-PySide6.QtQml)
[State Chart XML (SCXML): State Machine Notation for Control Abstraction](https://www.w3.org/TR/scxml/) supported by [PySide6.QtScxml](https://doc.qt.io/qtforpython-6/PySide6/QtScxml/index.html#module-PySide6.QtScxml)
[Rendering SVG Files](https://doc.qt.io/qtforpython-6/overviews/svgrendering.html#rendering-svg-files)
