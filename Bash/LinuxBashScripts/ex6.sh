#!/bin/bash

echo "Type something:"
read str

hebrew="אבגדהוזחטיכךלמםנןסעפףצץקרשת"
english="tcdsvuzjyhflknobixgp;m.era,"

if [[ $str == *["$hebrew"]* ]]
then
translate=$(echo "$str" | sed 'y/'$hebrew'/'$english'/')

elif [[ $str == *["$english"]* ]]
then
translate=$(echo "$str" | sed 'y/'$english'/'$hebrew'/')
fi

echo "$translate"
