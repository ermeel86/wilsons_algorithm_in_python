#!/bin/bash
PNG_NAME=$(python -c "print '$1'.replace('dot','png')")
dot -Kfdp -n -Tpng -o ${PNG_NAME} $1
