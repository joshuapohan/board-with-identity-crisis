cd static/board-client
npm install --only=dev && npm install && npm run build
cd ../../
cp -R static/board-client/build/static/. static/ 2> /dev/null
cp -R static/board-client/build/. static/ 2> /dev/null
ls static