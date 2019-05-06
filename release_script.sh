cd static/board-client
npm install --only=dev && npm install && npm run build
cd ../../
cp -r static/board-client/build/static/. static/
cp static/board-client/build/* static/