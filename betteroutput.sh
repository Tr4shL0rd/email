python3 deletusfetus.py > output.txt
if [ 'grep "Deleting " output.txt' ]; then
    python3 -c "from playsound import playsound; playsound('AUGH.wav')"
else
    [ -s output.txt ] || echo "file is empty" > output.txt
    if [ 'grep "file is empty" output.txt' ]; then
        echo no emails
    fi
fi