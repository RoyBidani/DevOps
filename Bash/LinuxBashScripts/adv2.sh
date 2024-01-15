#!/bin/bash

clipboard=$(xclip -o -selection clipboard)

hebrew="אבגדהוזחטיכךלמםנןסעפףצץקרשת"
english="tcdsvuzjyhflknobixgp;m.era,"

if [[ $clipboard == *["$hebrew"]* ]]
then
/home/shayt/trans he:en "$clipboard"

elif [[ $clipboard == *["$english"]* ]]
then
/home/shayt/trans en:he "$clipboard"
fi
