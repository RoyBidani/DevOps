#!/bin/bash

echo "Type something:"
read str

hebrew="אבגדהוזחטיכךלמםנןסעפףצץקרשת"
english="tcdsvuzjyhflknobixgp;m.era,"

if [[ $str == *["$hebrew"]* ]]
then
translate=$(echo "$str" | sed 'y/'$hebrew'/'$english'/')
xdotool key alt+shift

elif [[ $str == *["$english"]* ]]
then
translate=$(echo "$str" | sed 'y/'$english'/'$hebrew'/')
xdotool key alt+shift
fi

echo "$translate"

