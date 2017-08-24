# ----- Build Vips 8.5.7 w/ Python bindings -----

FROM roiavidan/amazon-linux-lambda-base:2016.03 AS buildenv

# Install devel dependencies
RUN sudo yum install -y gcc-c++ gobject-introspection-devel libtiff-devel fftw-devel libwebp-devel \
                        libexif-devel libjpeg-turbo-devel libpng-devel expat-devel lcms2-devel giflib-devel

# Install ORC which is not in Amazon repos
RUN sudo rpm -i http://dl.fedoraproject.org/pub/epel/6/x86_64/orc-0.4.16-6.el6.x86_64.rpm \
                http://dl.fedoraproject.org/pub/epel/6/x86_64/orc-compiler-0.4.16-6.el6.x86_64.rpm \
                http://dl.fedoraproject.org/pub/epel/6/x86_64/orc-devel-0.4.16-6.el6.x86_64.rpm

RUN sudo chmod 777 /usr/src

# Get Vips & PyVips source code
RUN curl -OLsk https://github.com/jcupitt/libvips/releases/download/v8.5.7/vips-8.5.7.tar.gz && \
    tar zxf vips-8.5.7.tar.gz -C /usr/src && \
    curl -OL https://github.com/jcupitt/pyvips/archive/master.zip && \
    unzip master.zip -d /usr/src

# Build VipsCC
RUN cd /usr/src/vips-8.5.7 && \
    ./configure --without-python --prefix=/tmp && \
    make -j`nproc` install-strip

# Deploy relevant binaries, libs and Python modules as build artifacts
RUN cd /tmp && mkdir -p artifacts/lib && \
    cp lib/libvips{,CC}.so.42 artifacts/lib/ && \
    ldd artifacts/lib/libvips.so.42 | awk '{print $3}' | grep -E 'exif|fftw|jbig|tiff|webp|orc' | xargs -i cp {} artifacts/lib/ && \
    pip install -t /tmp/ cffi && \
    cp -r /tmp/_cffi_backend.so /tmp/cffi /tmp/pycparser /tmp/artifacts/ && cp /tmp/.libs_cffi_backend/* /tmp/artifacts/lib/ && \
    sed -i 's/libvips.so/libvips.so.42/; s/libgobject-2.0.so/libgobject-2.0.so.0/' /usr/src/pyvips-master/pyvips/__init__.py && \
    cp -r /usr/src/pyvips-master/pyvips /tmp/artifacts/ && \
    rm -rf /tmp/artifacts/pyvips/tests


# ----- Development environment for AWS Lambda: resizer -----


# EC2 AMI used by Lambda ("close enough": http://docs.aws.amazon.com/lambda/latest/dg/current-supported-versions.html)
FROM roiavidan/amazon-linux-lambda-base:2016.03

# Install Python debugger & Unittest Mock library
RUN sudo pip install pudb mock

# Copy Vips artifacts from build environment
COPY --from=buildenv /tmp/artifacts/ /home/ec2-user

# Copy local files
COPY lambda.py /home/ec2-user/
COPY resizer/ /home/ec2-user/resizer/

RUN sudo chown -R ec2-user:users /home/ec2-user/*

CMD ["/bin/bash"]
