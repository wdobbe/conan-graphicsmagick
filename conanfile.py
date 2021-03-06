from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os
#from os import path, getcwd, environ
#import subprocess



class GraphicksMagickConan(ConanFile):
    name = "GraphicsMagick"
    version = "1.3.33"
    description = "GraphicsMagick is the swiss army knife of image processing. It provides tools and libraries which support reading, writing, and manipulating an image in over 88 major formats"
    url = "http://http://www.graphicsmagick.org/"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False], 
        "with_bzlib": [True, False],
        "with_jpeg": [True, False],
        "with_png": [True, False],
        "fPIC": [True, False]
    }
    default_options = "shared=True", "with_bzlib=True", "with_jpeg=True", "with_png=True", "fPIC=True", "libjpeg:shared=True", "libpng:shared=True"
    exports_sources = "CMakeLists.txt"
    license = "http://www.graphicsmagick.org/Copyright.html"
    source_subfolder = "GraphicsMagick-%s" % version
    short_paths = False

    def configure(self):
        if self.settings.compiler == 'Visual Studio':
            del self.options.fPIC

    def requirements(self):
        self.requires.add("zlib/1.2.11@conan/stable")
        self.requires.add("bzip2/1.0.8@conan/stable")
        if self.options.with_jpeg:
            self.requires.add("libjpeg/9c@bincrafters/stable")
        if self.options.with_png:
            self.requires.add("libpng/1.6.37@bincrafters/stable")

    def source(self):
        base_url = "https://downloads.sourceforge.net/project/graphicsmagick/graphicsmagick"
        tools.get("%s/%s/GraphicsMagick-%s.tar.bz2" % (base_url, self.version, self.version))

    def build(self):
        env_build = AutoToolsBuildEnvironment(self, win_bash=self.settings.os == 'Windows')
        env_build.fpic = True
        config_args = []
        if self.options.shared:
            config_args.extend(["--enable-shared=yes", "--enable-static=no"])
        else:
            config_args.extend(["--enable-shared=no", "--enable-static=yes"])
        if self.options.with_bzlib:
            config_args.append('--with-bzlib')
        else:
            config_args.append('--without-bzlib')
        if self.options.with_jpeg:
            config_args.append('--with-jpeg')
        else:
            config_args.append('--without-jpeg')
        if self.options.with_png:
            config_args.append('--with-png')
        else:
            config_args.append('--without-png')
        config_args.extend(["--without-dps", "--without-fpx", "--without-jbig", "--without-jp2", "--without-lcms2", "--without-lzma", "--with-magick-plus-plus", "--without-perl", "--without-trio", "--without-webp", "--without-wmf", "--with-zlib"])
        prefix = os.path.abspath(self.package_folder)
        if self.settings.os == 'Windows':
            prefix = tools.unix_path(prefix)
        config_args.append("--prefix=%s" % prefix)

        env_build_vars = env_build.vars
        #GM configure script links a program with jpeg lib and tries to run it. If libjpeg is a shared library, the dynamic linker must be able to find it
        if self.settings.os == 'Linux':
            env_build_vars['LD_LIBRARY_PATH'] = ""
            if self.options.with_jpeg:
                env_build_vars['LD_LIBRARY_PATH'] += self.deps_cpp_info["libjpeg"].lib_paths[0]
            if self.options.with_png:
                if len(env_build_vars['LD_LIBRARY_PATH']) != 0:
                    env_build_vars['LD_LIBRARY_PATH'] += ':'
                env_build_vars['LD_LIBRARY_PATH'] += self.deps_cpp_info["libpng"].lib_paths[0]
        print("configure with vars")
        print(env_build_vars['LD_LIBRARY_PATH'])

        env_build.configure(configure_dir=os.path.join(self.source_folder, self.source_subfolder), args=config_args, vars=env_build_vars)
        env_build.make()
        env_build.make(args=["install"])

    def package(self):
        self.copy("Copyright.txt", dst=self.package_folder, src=os.path.join(self.source_folder, "GraphicsMagick-%s" % self.version))

    def package_info(self):
        if self.settings.compiler == "Visual Studio":
            self.cpp_info.libs = ['libGraphicsMagick', 'libGraphicsMagickWand', 'libGraphicsMagick++']
        else:
            self.cpp_info.libs = ['GraphicsMagick', 'GraphicsMagickWand', 'GraphicsMagick++']
            if self.settings.os == "Linux":
                self.cpp_info.libdirs = ['lib', 'lib64']
