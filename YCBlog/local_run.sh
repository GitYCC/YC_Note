memcached -p 11212 &
pid_memcached=$!
cp ./YCBlog/settings.py.debug_True ./YCBlog/settings.py
python3 manage.py runserver 
cp ./YCBlog/settings.py.debug_False ./YCBlog/settings.py
kill -9 $pid_memcached
