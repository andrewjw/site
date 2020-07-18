module Jekyll

  class EnvironmentVariablesGenerator < Generator

    def generate(site)
      site.config['ga_id'] = ENV['GA_ID']
      # Add other environment variables to `site.config` here...
    end

  end

end
