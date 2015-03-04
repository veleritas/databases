#!/bin/bash
# last updated 2015-01-26 toby

files=('morbidmap')

echo "Updating: ${files[@]}"

./ftpOMIM.exp ${files[@]}

for fname in "${files[@]}"; do
	newname=$fname
	if [[ $fname != *".txt" ]]; then
		newname+=".txt"
	fi

	if [ -e "$fname" ]; then
		echo "Successfully got $fname"
		mv $fname ~/databases/omim/data/$newname
	else
		echo "Could not get $fname from OMIM server."
	fi
done

echo "Done."
