python create_tables.py
cd static/board-client
npm install --only=dev && npm install && npm run build
cp -R static/board-client/build/static/. static/
cp static/board-client/build/* static/