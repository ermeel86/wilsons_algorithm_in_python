#!/bin/bash
PDF_NAME=$(python -c "print '$1'.replace('dot','pdf')")
dot -Kfdp -n -Tpdf -o ${PDF_NAME} $1
okular ${PDF_NAME}
